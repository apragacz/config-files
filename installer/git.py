from __future__ import print_function, unicode_literals, division

from .base import copy_config_template, print_step


def prepare(installation):
    installation.require_params(['email'])


def configure(installation):
    print_step('Configuring git')
    copy_config_template(installation, '.gitconfig', param_names=['email'])
