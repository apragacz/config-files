from __future__ import print_function, unicode_literals, division
import os

from .base import print_info, print_step


def configure(installation):
    print_step('Installing Python CLI tools')
    print_info('Installing pipsi')
    os.system('curl https://raw.githubusercontent.com/mitsuhiko/pipsi/master/get-pipsi.py | python')  # noqa: E501
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
            print_info('Installing {package_name} via pipsi'.format(
                package_name=package_name))
            os.system('pipsi install {package_name}'.format(
                package_name=package_name))
