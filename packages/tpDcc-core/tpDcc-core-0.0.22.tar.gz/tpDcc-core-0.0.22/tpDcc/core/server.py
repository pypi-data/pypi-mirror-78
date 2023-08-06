import sys
import time
import json
import logging
import traceback
import importlib
from collections import OrderedDict
import __builtin__      # Do not remove

from Qt.QtCore import *
from Qt.QtWidgets import *
from Qt.QtNetwork import *

# We use to have autocompletion in PyCharm
if False:
    import tpDcc as tp


class DccServer(QObject, object):

    PORT = 17344
    HEADER_SIZE = 10

    def __init__(self, parent=None, client=None, update_paths=True):
        parent = parent or tp.Dcc.get_main_window()
        super(DccServer, self).__init__(parent)

        self._socket = None
        self._port = self.__class__.PORT
        self._do_update_paths = update_paths
        self._modules_to_import = list()
        self._client = client

        self._init()

    # =================================================================================================================
    # BASE
    # =================================================================================================================

    def select_node(self, data, reply):
        node = data.get('node', None)
        add_to_selection = data.get('add_to_selection', False)
        if node:
            tp.Dcc.select_object(node, replace_selection=not add_to_selection)
        reply['success'] = True

    def selected_nodes(self, data, reply):
        selected_nodes = tp.Dcc.selected_nodes()
        reply['success'] = True
        reply['result'] = selected_nodes

    def clear_selection(self, data, reply):
        tp.Dcc.clear_selection()
        reply['success'] = True

    def get_control_colors(self, data, reply):
        control_colors = tp.Dcc.get_control_colors() or list()
        reply['success'] = True
        reply['result'] = control_colors

    def get_fonts(self, data, reply):
        all_fonts = tp.Dcc.get_all_fonts() or list()
        reply['success'] = True
        reply['result'] = all_fonts

    def enable_undo(self, data, reply):
        tp.Dcc.enable_undo()
        reply['success'] = True

    def disable_undo(self, data, reply):
        tp.Dcc.disable_undo()
        reply['success'] = True

    # =================================================================================================================
    # INTERNAL
    # =================================================================================================================

    def _init(self):
        if self._client:
            return

        self._server = QTcpServer(self)
        self._server.newConnection.connect(self._on_established_connection)

        if self._listen():
            print('[LOG] Server listening on port: {}'.format(self._port))
        else:
            print('[ERROR] Server initialization failed')

    def _listen(self):
        if not self._server.isListening():
            return self._server.listen(QHostAddress.LocalHost, self._port)

        return False

    def _read(self):
        bytes_remaining = -1
        json_data = ''

        while self._socket.bytesAvailable():
            # header (10 bytes)
            if bytes_remaining <= 0:
                byte_array = self._socket.read(DccServer.HEADER_SIZE)
                bytes_remaining, valid = byte_array.toInt()
                if not valid:
                    bytes_remaining = -1
                    self._write_error('Invalid header')

                    # purge unknown data
                    self._socket.readAll()
                    return

            # body (payload)
            if bytes_remaining > 0:
                byte_array = self._socket.read(bytes_remaining)
                bytes_remaining -= len(byte_array)
                json_data += byte_array.data().decode()

                if bytes_remaining == 0:
                    bytes_remaining = -1
                    data = json.loads(json_data, object_pairs_hook=OrderedDict)
                    self._process_data(data)

                    json_data = ''

    def _write(self, reply_dict):
        json_reply = json.dumps(reply_dict)

        if self._socket and self._socket.state() == QTcpSocket.ConnectedState:
            header = '{0}'.format(len(json_reply.encode())).zfill(DccServer.HEADER_SIZE)
            data = QByteArray('{}{}'.format(header, json_reply).encode())
            self._socket.write(data)

        return json_reply

    def _write_error(self, error_msg):
        reply = {
            'success': False,
            'msg': error_msg,
            'cmd': 'unknown'
        }

        self._write(reply)

    def _process_data(self, data_dict):
        reply = {
            'success': False
        }

        cmd = data_dict['cmd']
        if cmd == 'ping':
            reply['success'] = True
        elif cmd == 'update_paths':
            self._update_paths(data_dict, reply)
        elif cmd == 'update_dcc_paths':
            self._update_dcc_paths(data_dict, reply)
        elif cmd == 'init_dcc':
            self._init_dcc(data_dict, reply)
        elif cmd == 'get_dcc_info':
            self._get_dcc_info(data_dict, reply)
        else:
            self._process_command(cmd, data_dict, reply)
            if not reply['success']:
                reply['cmd'] = cmd
                if 'msg' not in reply.keys():
                    reply['msg'] = 'Unknown Error'

        return self._write(reply)

    def _update_paths(self, data, reply):

        if not self._do_update_paths:
            reply['success'] = True
            reply['exe'] = sys.executable
            return

        paths_data = data.get('paths', dict())
        if not paths_data:
            reply['success'] = False
            return

        paths = paths_data.values()

        # NOTE: For now, we add the dependencies manually
        # In the final package, all dependencies libraries will be stored in a specific folder
        maya_deps_folder = r'D:\tpRigToolkit\venvs\maya_deps'
        paths.insert(0, maya_deps_folder)

        for path in paths:
            if path not in sys.path:
                print('Updating SYS.PATH: {}'.format(path))
                sys.path.append(path)

        for path_mod in paths_data.keys():
            try:
                mod = importlib.import_module(path_mod)
            except Exception:
                try:
                    print('FAILED IMPORT: {} -> {}'.format(str(path_mod), str(traceback.format_exc())))
                    continue
                except Exception:
                    print('FAILED IMPORT: {}'.format(path_mod))
                    continue
            self._modules_to_import.append(mod)

        reply['success'] = True
        reply['exe'] = sys.executable

    def _update_dcc_paths(self, data, reply):

        if not self._do_update_paths:
            reply['success'] = True
            return

        paths_data = data.get('paths', dict())
        if not paths_data:
            reply['success'] = False
            return

        paths = paths_data.values()

        for path in paths:
            if path not in sys.path:
                print('Updating SYS.PATH: {}'.format(path))
                sys.path.append(path)

        for path_mod in paths_data.keys():
            try:
                mod = importlib.import_module(path_mod)
            except Exception:
                try:
                    print('FAILED IMPORT: {} -> {}'.format(str(path_mod), str(traceback.format_exc())))
                    continue
                except Exception:
                    print('FAILED IMPORT: {}'.format(path_mod))
                    continue
            self._modules_to_import.append(mod)

        reply['success'] = True

    def _init_dcc(self, data, reply):
        if not self._modules_to_import:
            reply['success'] = False
            return

        modules_to_import = list()
        clean_modules_to_import = list(set(self._modules_to_import))

        # Order modules to import (tpDcc.core, tpDcc.dccs.X, etc)
        for module in clean_modules_to_import:
            if module.__name__ == 'tpDcc.loader' and module not in modules_to_import:
                modules_to_import.append(module)
                break
        for module in clean_modules_to_import:
            if module.__name__.startswith('tpDcc.dccs.') and module not in modules_to_import:
                modules_to_import.append(module)
        for module in clean_modules_to_import:
            if module not in self._modules_to_import:
                modules_to_import.append(module)

        for module in modules_to_import:
            if hasattr(module, 'init'):
                module.init()

        reply['success'] = True

    def _get_dcc_info(self, data, reply):

        import tpDcc

        bultins_ = {'tp': tpDcc}
        for builtin in bultins_:
            try:
                exec('del(__builtin__.%s)' % builtin)
            except Exception:
                pass
            builtin_value = bultins_[builtin]
            exec('__builtin__.%s = builtin_value' % builtin)

        # NOTE: tp is import dynamically
        dcc_name = tp.Dcc.get_name()
        dcc_version = tp.Dcc.get_version_name()

        reply['success'] = True
        reply['name'] = dcc_name
        reply['version'] = dcc_version

    def _process_command(self, command_name, data_dict, reply_dict):
        if command_name == 'select_node':
            self.select_node(data_dict, reply_dict)
        elif command_name == 'selected_nodes':
            self.selected_nodes(data_dict, reply_dict)
        elif command_name == 'clear_selection':
            self.clear_selection(data_dict, reply_dict)
        elif command_name == 'enable_undo':
            self.enable_undo(data_dict, reply_dict)
        elif command_name == 'disable_undo':
            self.disable_undo(data_dict, reply_dict)
        elif command_name == 'get_control_colors':
            self.get_control_colors(data_dict, reply_dict)
        elif command_name == 'get_fonts':
            self.get_fonts(data_dict, reply_dict)
        else:
            reply_dict['msg'] = 'Invalid command ({})'.format(command_name)

    # =================================================================================================================
    # CALLBACKS
    # =================================================================================================================

    def _on_established_connection(self):
        self._socket = self._server.nextPendingConnection()
        if self._socket.state() == QTcpSocket.ConnectedState:
            self._socket.disconnected.connect(self._on_disconnected)
            self._socket.readyRead.connect(self._read)
            print('[LOG] Connection established')

    def _on_disconnected(self):
        self._socket.disconnected.disconnect()
        self._socket.readyRead.disconnect()
        self._socket.deleteLater()
        print('[LOG] Connection disconnected')


class ExampleServer(DccServer, object):

    PORT = 17337

    def __init__(self, parent_window):
        super(ExampleServer, self).__init__(parent_window)

        self._window = parent_window

    def _process_command(self, command_name, data_dict, reply_dict):
        if command_name == 'echo':
            self.echo(data_dict, reply_dict)
        elif command_name == 'set_title':
            self.set_title(data_dict, reply_dict)
        elif command_name == 'sleep':
            self.sleep(data_dict, reply_dict)
        else:
            super(ExampleServer, self)._process_command(command_name, data_dict, reply_dict)

    def echo(self, data_dict, reply_dict):
        reply_dict['result'] = data_dict['text']
        reply_dict['success'] = True

    def set_title(self, data_dict, reply_dict):
        self._window.setWindowTitle(data_dict['title'])
        reply_dict['result'] = True
        reply_dict['success'] = True

    def sleep(self, data_dict, reply_dict):
        for i in range(6):
            print('Sleeping {}'.format(i))
            time.sleep(1)

        reply_dict['result'] = True
        reply_dict['success'] = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QDialog()
    window.setWindowTitle('Example Base')
    window.setFixedSize(240, 150)
    QPlainTextEdit(window)
    server = ExampleServer(window)
    window.show()
    app.exec_()
