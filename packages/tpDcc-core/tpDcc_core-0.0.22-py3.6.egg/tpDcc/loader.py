#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Initialization module for tpDcc
"""

from __future__ import print_function, division, absolute_import

import os
import importlib
import logging.config

from tpDcc import register
from tpDcc.abstract import dcc as abstract_dcc, menu as abstract_menu, shelf as abstract_shelf
from tpDcc.abstract import progressbar as abstract_progressbar
from tpDcc.managers import callbacks as callbacks_manager, configs as configs_manager, logs as logs_manager
from tpDcc.managers import menus as menus_manager, resources as resources_manager, tools as tools_manager

from tpDcc.libs.python import importer, loader as python_loader
from tpDcc.libs.qt import loader as qt_loader

# =================================================================================

PACKAGE = 'tpDcc'
main = __import__('__main__')

# =================================================================================


class DccCallbacks(object):
    Shutdown = ('Shutdown', {'type': 'simple'})
    Tick = ('Tick', {'type': 'simple'})
    ScenePreCreated = ('ScenePreCreated', {'type': 'simple'})
    ScenePostCreated = ('ScenePreCreated', {'type': 'simple'})
    SceneNewRequested = ('SceneNewRequested', {'type': 'simple'})
    SceneNewFinished = ('SceneNewFinished', {'type': 'simple'})
    SceneSaveRequested = ('SceneSaveRequested', {'type': 'simple'})
    SceneSaveFinished = ('SceneSaveFinished', {'type': 'simple'})
    SceneOpenRequested = ('SceneOpenRequested', {'type': 'simple'})
    SceneOpenFinished = ('SceneOpenFinished', {'type': 'simple'})
    UserPropertyPreChanged = ('UserPropertyPreChanged', {'type': 'filter'})
    UserPropertyPostChanged = ('UserPropertyPostChanged', {'type': 'filter'})
    NodeSelect = ('NodeSelect', {'type': 'filter'})
    NodeAdded = ('NodeAdded', {'type': 'filter'})
    NodeDeleted = ('NodeDeleted', {'type': 'filter'})


# =================================================================================


class Dccs(object):
    Unknown = 'unknown'
    Standalone = 'standalone'
    Maya = 'maya'
    Max = 'max'
    MotionBuilder = 'mobu'
    Houdini = 'houdini'
    Nuke = 'nuke'
    Unreal = 'unreal'

    @staticmethod
    def get_available_dccs():
        return {k: v for k, v in Dccs.__class__.__dict__.items() if not k.startswith('__')}

    packages = {
        'cmds': Maya,
        'MaxPlus': Max,
        'pyfbsdk': MotionBuilder,
        'hou': Houdini,
        'nuke': Nuke,
        'unreal': Unreal
    }


# =================================================================================

def init(dev=False):
    """
    Initializes module
    :param dev: bool, Whether tpDcc-core is initialized in dev mode or not
    """

    if dev:
        register.cleanup()
        importer.reload_module(register)
        importer.reload_module(callbacks_manager)
        importer.reload_module(python_loader)
        importer.reload_module(qt_loader)
        importer.reload_module(abstract_dcc)
        importer.reload_module(abstract_menu)
        importer.reload_module(abstract_shelf)
        importer.reload_module(abstract_progressbar)
        register_classes()

    logger = create_logger(dev=dev)

    register.register_class('logger', logger)

    callbacks_manager.CallbacksManager.cleanup()

    # try:
    #     if do_reload:
    #         # If we reload, we make sure that all tools and tpDcc windows are closed
    #         import tpDcc as tp
    #         tp.ToolsMgr().close_tools()
    #         parent = tp.Dcc.get_main_window()
    #         if parent:
    #             for child in parent.children():
    #                 if isinstance(child, tp.Window):
    #                     child.close()
    #                     child.setParent(None)
    #                     child.deleteLater()
    # except Exception:
    #     pass

    # We initialize first Python library
    python_loader.init(dev=dev)

    # We initialize then tpDcc-core library and DCC specific library
    # skip_modules = ['{}.{}'.format(PACKAGE, name) for name in ['loader', 'dccs', 'libs', 'tools']]
    # importer.init_importer(package=PACKAGE, skip_modules=skip_modules)

    # Get DCC
    dcc_mod = get_dcc_loader_module(logger=logger)
    logger.info('DCC module found: {}'.format(dcc_mod))
    if not dcc_mod:
        from tpDcc.dccs.standalone.core import dcc
        register.register_class('Dcc', dcc.StandaloneDcc)

    # Initialize current DCC modules
    if dcc_mod:
        dcc_mod.init_dcc(dev=dev)

    # After that, we initialize Qt library (we must do it after tpDcc one because tpDcc-libs-qt depends on tpDcc-core)
    # NOTE: DCC UI modules are automatically loaded by tpDcc-libs-qt
    qt_loader.init(dev=dev)

    init_managers(dev=dev)

    # # TODO: The initialization of extra libs should be managed by a specific LibManager
    # # Initialize tpDcc-libs-nameit
    # from tpDcc.libs.nameit import loader
    # loader.init(do_reload=do_reload)


def get_dcc_loader_module(package='tpDcc.dccs', logger=None):
    """
    Checks DCC we are working on an initializes proper variables
    """

    dcc_mod = None
    for dcc_package, dcc_name in Dccs.packages.items():
        if dcc_package in main.__dict__:
            module_to_import = '{}.{}.loader'.format(package, dcc_name)
            try:
                dcc_mod = importlib.import_module(module_to_import)
            except ImportError:
                if logger:
                    logger.warning('DCC module {} not found!'.format(module_to_import))
                continue
            if dcc_mod:
                break
    if not dcc_mod:
        try:
            import unreal
            try:
                dcc_mod = importlib.import_module('{}.unreal.loader')
            except ImportError:
                return None
        except Exception as exc:
            pass

    return dcc_mod


def init_managers(dev=True):
    """
    Initializes all tpDcc managers
    """

    import tpDcc
    from tpDcc import config
    from tpDcc import toolsets
    from tpDcc.managers import callbacks

    tpDcc.ConfigsMgr().register_package_configs(PACKAGE, os.path.dirname(config.__file__))

    core_config = tpDcc.ConfigsMgr().get_config('tpDcc-core')
    if not core_config:
        tpDcc.logger.warning(
            'tpDcc-core configuration file not found! Make sure that you have tpDcc-config package installed!')
        return None

    tools_to_load = core_config.get('tools', list())

    # Tools
    tpDcc.ToolsMgr().register_package_tools(pkg_name=PACKAGE, tools_to_register=tools_to_load, dev=dev)
    tpDcc.ToolsMgr().load_registered_tools(PACKAGE)

    # Toolsets
    tpDcc.ToolsetsMgr().register_path(PACKAGE, os.path.dirname(toolsets.__file__))
    tpDcc.ToolsetsMgr().load_registered_toolsets(PACKAGE, tools_to_load=tools_to_load)

    # Callbacks
    callbacks.CallbacksManager.initialize()


def create_logger(dev=False):
    """
    Returns logger of current module
    """

    logger_directory = os.path.normpath(os.path.join(os.path.expanduser('~'), PACKAGE, 'logs'))
    if not os.path.isdir(logger_directory):
        os.makedirs(logger_directory)

    logging_config = os.path.normpath(os.path.join(os.path.dirname(__file__), '__logging__.ini'))

    logging.config.fileConfig(logging_config, disable_existing_loggers=False)
    logger = logging.getLogger('tpDcc-core')
    if dev:
        logger.setLevel(logging.DEBUG)
        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)

    return logger


def is_unknown():
    """
    Check if current environment is unknown or not
    :return: bool
    """

    import tpDcc

    return tpDcc.Dcc.get_name() == Dccs.Unknown


def is_standalone():
    """
    Check if current environment is standalone or not
    :return: bool
    """

    import tpDcc

    return tpDcc.Dcc.get_name() == Dccs.Standalone


def is_maya():
    """
    Checks if Maya is available or not
    :return: bool
    """

    import tpDcc

    return tpDcc.Dcc.get_name() == Dccs.Maya


def is_max():
    """
    Checks if Max is available or not
    :return: bool
    """

    import tpDcc

    return tpDcc.Dcc.get_name() == Dccs.Max


def is_mobu():
    """
    Checks if MotionBuilder is available or not
    :return: bool
    """

    import tpDcc

    return tpDcc.Dcc.get_name() == Dccs.MotionBuilder


def is_houdini():
    """
    Checks if Houdini is available or not
    :return: bool
    """

    import tpDcc

    return tpDcc.Dcc.get_name() == Dccs.Houdini


def is_unreal():
    """
    Checks if Houdini is available or not
    :return: bool
    """

    import tpDcc

    return tpDcc.Dcc.get_name() == Dccs.Unreal


def is_nuke():
    """
    Checks if Nuke is available or not
    :return: bool
    """

    import tpDcc

    return tpDcc.Dcc.get_name() == Dccs.Nuke


def callbacks():
    """
    Return a full list of callbacks based on DccCallbacks dictionary
    :return: list<str>
    """

    new_list = list()
    for k, v in DccCallbacks.__dict__.items():
        if k.startswith('__') or k.endswith('__'):
            continue
        new_list.append(v[0])

    return new_list


# =================================================================================

def register_classes():
    register.register_class('Dcc', abstract_dcc.AbstractDCC(), is_unique=True)
    register.register_class('Menu', abstract_menu.AbstractMenu, is_unique=True)
    register.register_class('Shelf', abstract_shelf.AbstractShelf, is_unique=True)
    register.register_class('ProgressBar', abstract_progressbar.AbstractProgressBar, is_unique=True)
    register.register_class('Dccs', Dccs)
    register.register_class('DccCallbacks', DccCallbacks)
    register.register_class('callbacks', callbacks)
    register.register_class('is_unknown', is_unknown)
    register.register_class('is_standalone', is_standalone)
    register.register_class('is_maya', is_maya)
    register.register_class('is_max', is_max)
    register.register_class('is_houdini', is_houdini)
    register.register_class('is_nuke', is_nuke)
    register.register_class('is_unreal', is_unreal)
    register.register_class('get_dcc_loader_module', get_dcc_loader_module)
    register.register_class('CallbacksMgr', callbacks_manager.CallbacksManager)
    register.register_class('ConfigsMgr', configs_manager.ConfigsManagerSingleton)
    register.register_class('LogsMgr', logs_manager.LogsManagerSingleton)
    register.register_class('MenusMgr', menus_manager.MenusManagerSingleton)
    register.register_class('ResourcesMgr', resources_manager.ResourcesManagerSingleton)
    register.register_class('ToolsMgr', tools_manager.ToolsManagerSingleton)


register_classes()
