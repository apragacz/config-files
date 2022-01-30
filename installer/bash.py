from __future__ import print_function, unicode_literals, division
import os.path

from .base import append_config_line, print_step


def configure(installation):
    print_step('Configuring bash')
    bashrc_ext_path = os.path.join(installation.files_path, '.bashrc_ext')
    line = 'source {bashrc_ext_path}'.format(bashrc_ext_path=bashrc_ext_path)
    append_config_line(installation, '.bashrc', line)
