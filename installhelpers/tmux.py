from __future__ import print_function, unicode_literals, division

from .base import create_config_symlink


def configure(installation):
    create_config_symlink(installation, '.tmux.conf')
