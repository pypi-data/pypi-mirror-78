#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Artella Uninstall plugin implementation
"""

from __future__ import print_function, division, absolute_import

import os
import sys
import logging

import artella
import artella.dcc as dcc
import artella.loader as loader
from artella.core import plugin, utils, qtutils

logger = logging.getLogger('artella')


class UninstallerPlugin(plugin.ArtellaPlugin, object):

    ID = 'artella-plugins-uninstaller'
    INDEX = 100

    def __init__(self, config_dict=None, manager=None):
        super(UninstallerPlugin, self).__init__(config_dict=config_dict, manager=manager)

    def uninstall(self, show_dialogs=True):
        artella_path = artella.__path__[0]
        if not os.path.isdir(artella_path):
            msg = 'Artella folder "{}" does not exists!'.format(artella_path)
            if show_dialogs:
                artella.DccPlugin().show_warning_message(text=msg)
            else:
                logger.warning(msg)
            return False

        res = qtutils.show_question_message_box(
            'Artella Uninstaller',
            'All plugins will be removed.\n\nArtella plugin will not be accessible by any DCC after uninstall.\n\n'
            'Are you sure you want to uninstall Artella Plugin?')
        if not res:
            return False

        do_remove_install_folder = not artella.DccPlugin().dev

        valid_uninstall = self._uninstall(artella_path)
        if not valid_uninstall:
            msg = 'Artella uninstall process was not completed!'.format(artella_path)
            if show_dialogs:
                artella.DccPlugin().show_error_message(text=msg)
            else:
                logger.error(msg)
            return False

        loader.shutdown(dev=False)

        if do_remove_install_folder:
            try:
                logger.info('Removing Artella Dcc Plugin directory: {}'.format(artella_path))
                utils.delete_folder(artella_path)
            except Exception as exc:
                logger.warning(
                    'Impossible to remove Artella Dcc plugin directory: {} | {}'.format(artella_path, exc))
                return False

        if os.path.isdir(artella_path):
            msg = 'Artella folder was not removed during uninstall process.\n\n{}\n\n Remove it manually if you ' \
                  'want to have a complete clean uninstall of Artella plugin.'.format(artella_path)
            if show_dialogs:
                dcc.show_info('Artella Uninstaller', msg)
            else:
                logger.info(msg)
            utils.open_folder(os.path.dirname(artella_path))

        # Remove specific DCC install folder if exists
        root_dcc_install_dir = os.path.dirname(os.path.dirname(os.path.dirname(artella_path)))
        dcc_install_dir = os.path.join(root_dcc_install_dir, dcc.name())
        if os.path.isdir(dcc_install_dir):
            utils.delete_folder(dcc_install_dir)

        # Cleanup artella directories from
        artella_dir = os.path.dirname(artella_path)
        sys_paths = [artella_path, artella_dir, utils.clean_path(artella_path), utils.clean_path(artella_dir)]
        paths_to_remove = list()
        for sys_path in sys.path:
            if sys_path in sys_paths:
                paths_to_remove.append(sys_path)
                sys.path.remove(sys_path)
            elif 'artella-plugins' in sys_path or 'artella-dccs' in sys_path:
                paths_to_remove.append(sys_path)
        for path_to_remove in paths_to_remove:
            if path_to_remove not in sys.path:
                continue
            sys.path.remove(path_to_remove)

        return True

    def _uninstall(self, artella_path):
        return True
