import os
import sys
import time
import json
import socket
import pkgutil
import traceback
from collections import OrderedDict

from Qt.QtCore import *

import tpDcc.loader
import tpDcc.config
import tpDcc.libs.python.loader
import tpDcc.libs.qt.loader
from tpDcc.libs.python import python, path as path_utils

if sys.version_info[0] == 2:
    from socket import error as ConnectionRefusedError


class DccClientSignals(QObject, object):
    dccDisconnected = Signal()


class DccClient(object):

    PORT = 17344
    HEADER_SIZE = 10

    signals = DccClientSignals()

    def __init__(self, timeout=10):
        self._timeout = timeout
        self._port = self.__class__.PORT
        self._discard_count = 0
        self._server = None

    # =================================================================================================================
    # BASE
    # =================================================================================================================

    def set_server(self, server):
        self._server = server

    def connect(self, port=-1):
        if self._server:
            return True

        if port > 0:
            self._port = port
        try:
            self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._client_socket.connect(('localhost', self._port))
            self._client_socket.setblocking(0)
        except ConnectionRefusedError as exc:
            tpDcc.logger.warning(exc)
            return False
        except Exception:
            tpDcc.logger.exception(traceback.format_exc())
            return False

        return True

    def disconnect(self):
        try:
            self._client_socket.close()
            self.signals.dccDisconnected.emit()
        except Exception:
            traceback.print_exc()
            return False

        return True

    def send(self, cmd_dict):
        json_cmd = json.dumps(cmd_dict)

        # If we use execute the tool inside DCC we execute client/server in same process. We can just launch the
        # function in the server
        if self._server:
            reply_json = self._server._process_data(cmd_dict)
            if not reply_json:
                return {'success': False}
            return json.loads(reply_json)
        else:
            message = list()
            message.append('{0:10d}'.format(len(json_cmd.encode())))    # header (10 bytes)
            message.append(json_cmd)

            try:
                msg_str = ''.join(message)
                self._client_socket.sendall(msg_str.encode())
            except OSError as exc:
                tpDcc.logger.debug(exc)
                return None
            except Exception:
                tpDcc.logger.exception(traceback.format_exc())
                return None

            return self.recv()

    def recv(self):
        total_data = list()
        data = ''
        reply_length = 0
        bytes_remaining = DccClient.HEADER_SIZE

        start_time = time.time()
        while time.time() - start_time < self._timeout:
            try:
                data = self._client_socket.recv(bytes_remaining)
            except Exception as exc:
                time.sleep(0.01)
                print(exc)
                continue

            if data:
                total_data.append(data)
                bytes_remaining -= len(data)
                if bytes_remaining <= 0:
                    for i in range(len(total_data)):
                        total_data[i] = total_data[i].decode()

                    if reply_length == 0:
                        header = ''.join(total_data)
                        reply_length = int(header)
                        bytes_remaining = reply_length
                        total_data = list()
                    else:
                        if self._discard_count > 0:
                            self._discard_count -= 1
                            return self.recv()

                        reply_json = ''.join(total_data)
                        return json.loads(reply_json)

        self._discard_count += 1

        raise RuntimeError('Timeout waiting for response')

    def is_valid_reply(self, reply_dict):
        if not reply_dict:
            tpDcc.logger.debug('Invalid reply')
            return False

        if not reply_dict['success']:
            tpDcc.logger.error('{} failed: {}'.format(reply_dict['cmd'], reply_dict['msg']))
            return False

        return True

    def ping(self):
        cmd = {
            'cmd': 'ping'
        }

        reply = self.send(cmd)

        if not self.is_valid_reply(reply):
            return False

        return True

    def update_paths(self):

        paths_to_update = self._get_paths_to_update()

        cmd = {
            'cmd': 'update_paths',
            # NOTE: The order is SUPER important, we must load the modules in the client in the same order
            'paths': OrderedDict(paths_to_update)
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return False

        exe = reply_dict.get('exe', None)

        return reply_dict['success'], exe

    def update_dcc_paths(self, dcc_executable):
        if not dcc_executable:
            return False

        dcc_name = None
        if 'maya' in dcc_executable:
            dcc_name = 'maya'
        elif '3dsmax' in dcc_executable:
            dcc_name = 'max'
        elif 'houdini' in dcc_executable:
            dcc_name = 'houdini'
        elif 'nuke' in dcc_executable:
            dcc_name = 'nuke'
        elif 'unreal' in dcc_executable:
            dcc_name = 'unreal'
        if not dcc_name:
            tpDcc.logger.warning('Executable DCC {} is not supported!'.format(dcc_executable))
            return False

        module_name = 'tpDcc.dccs.{}.loader'.format(dcc_name)
        try:
            mod = pkgutil.get_loader(module_name)
        except Exception:
            try:
                tpDcc.logger.error('FAILED IMPORT: {} -> {}'.format(str(module_name), str(traceback.format_exc())))
                return
            except Exception:
                tpDcc.logger.error('FAILED IMPORT: {}'.format(module_name))
                return
        if not mod:
            tpDcc.logger.warning('Impossible to import DCC specific module: {} ({})'.format(module_name, dcc_name))
            return False

        cmd = {
            'cmd': 'update_dcc_paths',
            'paths': OrderedDict({
                'tpDcc.dccs.{}'.format(dcc_name): path_utils.clean_path(
                    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(mod.filename)))))
            })
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return False

        return reply_dict['success']

    def init_dcc(self):
        cmd = {
            'cmd': 'init_dcc'
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return False

        return reply_dict['success']

    def get_dcc_info(self):
        cmd = {
            'cmd': 'get_dcc_info'
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return None, None

        return reply_dict['name'], reply_dict['version']

    def select_node(self, node, add_to_selection=False):
        cmd = {
            'cmd': 'select_node',
            'node': python.force_list(node),
            'add_to_selection': add_to_selection
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return False

        return reply_dict['success']

    def selected_nodes(self):
        cmd = {
            'cmd': 'selected_nodes'
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict.get('result', list())

    def clear_selection(self):
        cmd = {
            'cmd': 'clear_selection'
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return False

        return reply_dict['success']

    def get_control_colors(self):
        cmd = {
            'cmd': 'get_control_colors'
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict.get('result', list())

    def get_fonts(self):
        cmd = {
            'cmd': 'get_fonts'
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict.get('result', list())

    def enable_undo(self):
        cmd = {
            'cmd': 'enable_undo'
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def disable_undo(self):
        cmd = {
            'cmd': 'disable_undo'
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def _get_paths_to_update(self):
        """
        Internal function that returns all the paths that DCC server should include to properly work with the client
        """

        return {
            'tpDcc.loader': path_utils.clean_path(os.path.dirname(os.path.dirname(tpDcc.loader.__file__))),
            'tpDcc.config': path_utils.clean_path(
                os.path.dirname(os.path.dirname(os.path.dirname(tpDcc.config.__file__)))),
            'tpDcc.libs.python.loader': path_utils.clean_path(
                os.path.dirname(
                    os.path.dirname(os.path.dirname(os.path.dirname(tpDcc.libs.python.loader.__file__))))),
            'tpDcc.libs.qt.loader': path_utils.clean_path(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(tpDcc.libs.qt.loader.__file__)))))
        }


class ExampleClient(DccClient, object):

    PORT = 17337

    def echo(self, text):
        cmd_dict = {
            'cmd': 'echo',
            'text': text
        }

        reply_dict = self.send(cmd_dict)

        if not self.is_valid_reply(reply_dict):
            return None

        return reply_dict['result']

    def set_title(self, title):
        cmd_dict = {
            'cmd': 'set_title',
            'title': title
        }

        reply_dict = self.send(cmd_dict)

        if not self.is_valid_reply(reply_dict):
            return None

        return reply_dict['result']

    def sleep(self):
        cmd_dict = {
            'cmd': 'sleep'
        }

        reply_dict = self.send(cmd_dict)

        if not self.is_valid_reply(reply_dict):
            return None

        return reply_dict['result']


if __name__ == '__main__':
    client = ExampleClient(timeout=10)
    if client.connect():
        print('Connected successfully!')

        print(client.ping())
        print(client.echo('Hello World!'))
        print(client.set_title('New Server Title'))
        print(client.sleep())

        if client.disconnect():
            print('Disconnected successfully!')
    else:
        print('Failed to connect')
