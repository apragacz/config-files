from __future__ import print_function, unicode_literals, division
import os

from .base import print_info, print_step


def configure(installation):
    print_step('Installing Python CLI tools')
    print_info('Installing pipx')
    if installation.os_name == 'darwin':
        os.system('brew install pipx')
        os.system('pipx ensurepath')
        pipsi_path = '/usr/local/bin/pipx'
    else:
        os.system('python -m pip install --user pipx')
        os.system('python -m pipx ensurepath')
        pipsi_path = os.path.join(
            installation.home_path, '.local', 'bin', 'pipx')
    reqs_path = os.path.join(
        installation.repo_path, 'dependencies', 'pipsi', 'base.txt')
    with open(reqs_path, 'rt') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'):
                continue
            package_name = line
            print_info('Installing {package_name} via pipx'.format(
                package_name=package_name))
            os.system('{pipsi_path} install {package_name}'.format(
                pipsi_path=pipsi_path,
                package_name=package_name))
