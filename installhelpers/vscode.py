from __future__ import print_function, unicode_literals, division
import os

from .base import (
    create_config_symlink, print_step, yield_valid_lines_from_filename)


def install_extenstion(installation, extension_name):
    os.system("code --install-extension {extension_name}".format(
        extension_name=extension_name))


def install_extensions(installation):
    extensions_list_filepath = os.path.join(
        installation.repo_path, 'dependencies', 'vscode', 'base.txt')
    for ext_name in yield_valid_lines_from_filename(extensions_list_filepath):
        install_extenstion(installation, ext_name)


def configure(installation):
    print_step('Configuring VS Code')
    create_config_symlink(installation, '.config/Code/User/settings.json')
    install_extensions(installation)
