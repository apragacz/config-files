from __future__ import print_function, unicode_literals, division

from .base import copy_config_template


def configure(installation):
    copy_config_template(installation, '.gitconfig', ['email'])
