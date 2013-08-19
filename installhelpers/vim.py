import os
import shutil

from os.path import join as pjoin

from .base import (print_step, print_info)

HOME_DIRPATH = os.environ['HOME']


def copy_config_files():
    print_step(u'Copying ViM config files')
    src_dirname = 'files/vim/config'
    filename = '.vimrc'
    print_info(u'Copying {}'.format(filename))
    shutil.copyfile(pjoin(src_dirname, filename),
                    pjoin(HOME_DIRPATH, filename))
    pass


def configure():
    copy_config_files()
