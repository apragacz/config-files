from __future__ import print_function, unicode_literals, division

from .base import copy_config_template, print_step


def ask_for_params(installation):
    installation.ask_for_params(['email'])


def configure(installation):
    print_step('Configuring git')
    copy_config_template(installation, '.gitconfig', ['email'])
