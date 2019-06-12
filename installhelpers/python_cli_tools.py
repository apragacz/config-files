from __future__ import print_function, unicode_literals, division
import os

from .base import print_info, print_step


def configure(installation):
    print_step('Installing Python CLI tools')
    print_info('Installing pipsi')
    os.system('curl -O https://raw.githubusercontent.com/mitsuhiko/pipsi/master/get-pipsi.py')  # noqa: E501
    os.system('python get-pipsi.py --src=git+https://github.com/mitsuhiko/pipsi.git')  # noqa: E501
    os.system('rm get-pipsi.py')
    reqs_path = os.path.join(
        installation.repo_path, 'dependencies', 'pipsi', 'base.txt')
    pipsi_path = os.path.join(
        installation.home_path, '.local', 'bin', 'pipsi')
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
            os.system('{pipsi_path} install {package_name}'.format(
                pipsi_path=pipsi_path,
                package_name=package_name))
