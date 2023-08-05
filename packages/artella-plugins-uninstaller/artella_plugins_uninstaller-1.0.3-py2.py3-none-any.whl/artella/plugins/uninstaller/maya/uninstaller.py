#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Artella Uninstaller plugin implementation for Maya
"""

from __future__ import print_function, division, absolute_import

import os
import logging

from artella.core import utils
from artella.plugins.uninstaller import uninstaller

ARTELLA_MOD_NAMES = ['artella.mod']

logger = logging.getLogger('artella')


class UninstallerMayaPlugin(uninstaller.UninstallerPlugin, object):
    def __init__(self, config_dict=None, manager=None):
        super(UninstallerMayaPlugin, self).__init__(config_dict=config_dict, manager=manager)

    def _uninstall(self, artella_path):
        super(UninstallerMayaPlugin, self)._uninstall(artella_path)

        maya_module_paths = os.environ.get('MAYA_MODULE_PATH', None)
        if not maya_module_paths:
            logger.warning('No Maya module paths found ...')
            return False

        module_files_to_remove = list()

        maya_module_paths = maya_module_paths.split(os.pathsep)
        for maya_module_path in maya_module_paths:
            if maya_module_path and os.path.isdir(maya_module_path):
                try:
                    module_files = os.listdir(maya_module_path)
                    for module_file in module_files:
                        if module_file in ARTELLA_MOD_NAMES:
                            module_file_to_remove = os.path.join(maya_module_path, module_file)
                            module_files_to_remove.append(module_file_to_remove)
                except Exception as exc:
                    continue
        if not module_files_to_remove:
            logger.warning('No Artella Maya module file found ...')
            return False

        logger.info('Removing Artella Maya module files: {}'.format(module_files_to_remove))
        valid_remove = False
        for module_file_to_remove in module_files_to_remove:
            if not os.path.isfile(module_file_to_remove):
                continue
            valid_remove = utils.delete_file(module_file_to_remove)
            if not valid_remove:
                logger.error('Was impossible to remove Artella module file: {}'.format(module_file_to_remove))
                break
            else:
                logger.info('Artella Maya module files: {} removed successfully!'.format(module_file_to_remove))

        # We also make sure that we remove the userSetup.py file
        user_setup_py_file = os.path.join(os.path.dirname(artella_path), 'userSetup.py')
        if os.path.isfile(user_setup_py_file):
            removed_user_setup = utils.delete_file(user_setup_py_file)
            if not removed_user_setup:
                logger.warning('Was impossible to remove Artella userSetup.py file: {}!'.format(removed_user_setup))

        return valid_remove
