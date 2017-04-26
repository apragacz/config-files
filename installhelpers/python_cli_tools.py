from __future__ import print_function, unicode_literals, division
import os

from .base import print_step


def configure(installation):
    print_step('Installing Python CLI tools')
    reqs_path = os.path.join(installation.repo_path, 'pip-packages',
                             'general-cli-tools.txt')
    os.system('pip install -r {reqs_path}'.format(reqs_path=reqs_path))
