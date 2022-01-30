from __future__ import print_function, unicode_literals, division
import os
import subprocess

from .base import (
    create_config_symlink, ensure_home_dirpath_created, print_info, print_step,
    yield_valid_lines_from_filename)


def install_extenstion(installation, extension_name):
    os.system("code --install-extension {extension_name}".format(
        extension_name=extension_name))


def install_extensions(installation):
    for category in ['base', 'bash-development', 'python-development']:
        print_info(f"Installing {category} extensions")
        extensions_list_filepath = os.path.join(
            installation.repo_path, 'dependencies', 'vscode', f'{category}.txt')
        for ext_name in yield_valid_lines_from_filename(extensions_list_filepath):
            install_extenstion(installation, ext_name)


def configure(installation):
    print_step('Configuring VS Code')
    ensure_home_dirpath_created(installation, '.config/Code/User')
    create_config_symlink(installation, '.config/Code/User/settings.json')
    install_extensions(installation)


def prepare(installation):
    print_step('Preparing VS Code configuration')
    try:
        subprocess.check_output(['/usr/bin/env', 'which', 'code'])
    except subprocess.CalledProcessError:
        print_info('Code executable not found, ommitting')
        return False
