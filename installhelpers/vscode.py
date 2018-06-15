from __future__ import print_function, unicode_literals, division
import os
import subprocess

from .base import (
    create_config_symlink, print_info, print_step,
    yield_valid_lines_from_filename)


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


def prepare(installation):
    print_step('Preparing VS Code configuration')
    try:
        result = subprocess.check_output(['/usr/bin/env', 'which', 'code'])
    except subprocess.CalledProcessError:
        print_info('Code executable not found, ommitting')
        return False
