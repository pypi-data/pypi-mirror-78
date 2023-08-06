#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains DCC functionality for standalone applications
"""

from __future__ import print_function, division, absolute_import

import tpDcc
from tpDcc import register
from tpDcc.abstract import dcc as abstract_dcc
from tpDcc.libs.python import python, decorators

from Qt.QtWidgets import *


class StandaloneDcc(abstract_dcc.AbstractDCC, object):

    @staticmethod
    def get_name():
        """
        Returns the name of the DCC
        :return: str
        """

        return tpDcc.Dccs.Standalone

    @staticmethod
    def get_extensions():
        """
        Returns supported extensions of the DCC
        :return: list(str)
        """

        return []

    @staticmethod
    def get_dpi(value=1):
        """
        Returns current DPI used by DCC
        :param value: float
        :return: float
        """

        return 1.0

    @staticmethod
    def get_dpi_scale(value):
        """
        Returns current DPI scale used by DCC
        :return: float
        """

        return 1.0

    @staticmethod
    def get_version():
        """
        Returns version of the DCC
        :return: int
        """

        return 0

    @staticmethod
    def get_version_name():
        """
        Returns version of the DCC
        :return: str
        """

        return '0.0.0'

    @staticmethod
    def is_batch():
        """
        Returns whether DCC is being executed in batch mode or not
        :return: bool
        """

        return False

    @staticmethod
    def enable_component_selection():
        """
        Enables DCC component selection mode
        """

        pass

    @staticmethod
    def get_main_window():
        """
        Returns Qt object that references to the main DCC window
        :return:
        """

        return None

    @staticmethod
    def get_main_menubar():
        """
        Returns Qt object that references to the main DCC menubar
        :return:
        """

        return None

    @staticmethod
    def execute_deferred(fn):
        """
        Executes given function in deferred mode
        """

        return fn()

    @staticmethod
    def new_scene(force=True, do_save=True):
        """
        Creates a new DCC scene
        :param force: bool, True if we want to save the scene without any prompt dialog
        :param do_save: bool, True if you want to save the current scene before creating new scene
        :return:
        """

        return None

    @staticmethod
    def object_exists(node):
        """
        Returns whether given object exists or not
        :return: bool
        """

        return False

    @staticmethod
    def object_type(node):
        """
        Returns type of given object
        :param node: str
        :return: str
        """

        return None

    @staticmethod
    def check_object_type(node, node_type, check_sub_types=False):
        """
        Returns whether give node is of the given type or not
        :param node: str
        :param node_type: str
        :param check_sub_types: bool
        :return: bool
        """

        return False

    @staticmethod
    def node_is_empty(node, *args, **kwargs):
        """
        Returns whether given node is an empty one.
        In Maya, an emtpy node is the one that is not referenced, has no child transforms, has no custom attributes
        and has no connections
        :param node: str
        :return: bool
        """

        return True

    @staticmethod
    def node_is_transform(node):
        """
        Returns whether or not given node is a transform node
        :param node: str
        :return: bool
        """

        return False

    @staticmethod
    def all_scene_objects(full_path=True):
        """
        Returns a list with all scene nodes
        :param full_path: bool
        :return: list<str>
        """

        return list()

    @staticmethod
    def rename_node(node, new_name, **kwargs):
        """
        Renames given node with new given name
        :param node: str
        :param new_name: str
        :return: str
        """

        return False

    @staticmethod
    def rename_transform_shape_nodes(node):
        """
        Renames all shape nodes of the given transform node
        :param node: str
        """

        return False

    @staticmethod
    def show_object(node):
        """
        Shows given object
        :param node: str
        """

        return False

    @staticmethod
    def select_object(node, replace_selection=True, **kwargs):
        """
        Selects given object in the current scene
        :param replace_selection: bool
        :param node: str
        """

        return False

    @staticmethod
    def select_hierarchy(root=None, add=False):
        """
        Selects the hierarchy of the given node
        If no object is given current selection will be used
        :param root: str
        :param add: bool, Whether new selected objects need to be added to current selection or not
        """

        return False

    @staticmethod
    def deselect_object(node):
        """
        Deselects given node from current selection
        :param node: str
        """

        return False

    @staticmethod
    def clear_selection():
        """
        Clears current scene selection
        """

        return False

    @staticmethod
    def duplicate_object(node, name='', only_parent=False):
        """
        Duplicates given object in current scene
        :param node: str
        :param name: str
        :param only_parent: bool, If True, only given node will be duplicated (ignoring its children)
        :return: str
        """

        return False

    @staticmethod
    def delete_object(node):
        """
        Removes given node from current scene
        :param node: str
        """

        return False

    @staticmethod
    def clean_construction_history(node):
        """
        Removes the construction history of the given node
        :param node: str
        """

        return False

    @staticmethod
    def selected_nodes(full_path=True, **kwargs):
        """
        Returns a list of selected nodes
        :param full_path: bool
        :return: list<str>
        """

        return list()

    @staticmethod
    def selected_nodes_of_type(node_type, full_path=True):
        """
        Returns a list of selected nodes of given type
        :param node_type: str
        :param full_path: bool
        :return: list(str)
        """

        return list()

    @staticmethod
    def selected_hilited_nodes(full_path=True):
        """
        Returns a list of selected nodes that are hilited for component selection
        :param full_path: bool
        :return: list(str)
        """

        return list()

    @staticmethod
    def confirm_dialog(title, message, button=None, cancel_button=None, default_button=None, dismiss_string=None):
        """
        Shows DCC confirm dialog
        :param title:
        :param message:
        :param button:
        :param cancel_button:
        :param default_button:
        :param dismiss_string:
        :return:
        """

        from tpDcc.libs.qt.widgets import messagebox

        new_buttons = None
        if button:
            if python.is_string(button):
                if button == 'Yes':
                    new_buttons = QDialogButtonBox.Yes
                elif button == 'No':
                    new_buttons = QDialogButtonBox.No
            elif isinstance(button, (tuple, list)):
                for i, btn in enumerate(button):
                    if i == 0:
                        if btn == 'Yes':
                            new_buttons = QDialogButtonBox.Yes
                        elif btn == 'No':
                            new_buttons = QDialogButtonBox.No
                    else:
                        if btn == 'Yes':
                            new_buttons = new_buttons | QDialogButtonBox.Yes
                        elif btn == 'No':
                            new_buttons = new_buttons | QDialogButtonBox.No
        if new_buttons:
            buttons = new_buttons
        else:
            buttons = button or QDialogButtonBox.Yes | QDialogButtonBox.No

        if cancel_button:
            if python.is_string(cancel_button):
                if cancel_button == 'No':
                    buttons = buttons | QDialogButtonBox.No
                elif cancel_button == 'Cancel':
                    buttons = buttons | QDialogButtonBox.Cancel
            else:
                buttons = buttons | QDialogButtonBox.Cancel

        return messagebox.MessageBox.question(None, title=title, text=message, buttons=buttons)

    @staticmethod
    def warning(message):
        """
        Prints a warning message
        :param message: str
        :return:
        """

        print('WARNING: {}'.format(message))

    @staticmethod
    def error(message):
        """
        Prints a error message
        :param message: str
        :return:
        """

        print('ERROR: {}'.format(message))

    @staticmethod
    def get_control_colors():
        """
        Returns control colors available in DCC
        :return: list(float, float, float)
        """

        return []

    @staticmethod
    def get_all_fonts():
        """
        Returns all fonts available in DCC
        :return: list(str)
        """

        # TODO: We can use Qt to retrieve system fonts
        return []

    @staticmethod
    def get_undo_decorator():
        """
        Returns undo decorator for current DCC
        """

        return decorators.empty_decorator

    @staticmethod
    def get_repeat_last_decorator(command_name=None):
        """
        Returns repeat last decorator for current DCC
        """

        return decorators.empty_decorator

    @staticmethod
    def deferred_function(fn, *args, **kwargs):
        """
        Calls given function with given arguments in a deferred way
        :param fn:
        :param args: list
        :param kwargs: dict
        """

        return fn(*args, **kwargs)


register.register_class('Dcc', StandaloneDcc)
