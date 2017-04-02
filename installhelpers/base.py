from __future__ import print_function, unicode_literals, division
import contextlib
import json
import os

import six.moves
import jinja2


def yield_valid_lines_from_filename(filepath):
    with open(filepath, 'rt') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line[0] == '#':
                continue
            yield line


def print_step(text):
    print('>>> {text}'.format(text=text))


def print_info(text):
    print('    {text}'.format(text=text))


def load_json_config(filepath, default=None):
    try:
        with open(filepath, 'rt') as f:
            return json.load(f)
    except IOError:
        # file not found, return fallback value
        return default


def save_json_config(filepath, config):
    with open(filepath, 'wt') as f:
        json.dump(config, f)


def ensure_dirpath_created(dirpath):
    if not (os.path.exists(dirpath) and os.path.isdir(dirpath)):
        os.makedirs(dirpath)


@contextlib.contextmanager
def chdir(dir_path):
    olddir_path = os.getcwd()
    os.chdir(dir_path)
    yield
    os.chdir(olddir_path)


class Installation(object):

    def __init__(self, home_path, repo_path, params={}):
        self.home_path = home_path
        self.repo_path = repo_path
        self._params = params

    @property
    def files_path(self):
        return os.path.join(self.repo_path, 'files')

    def get_params(self, names):
        for name in names:
            if name not in self._params:
                self._params[name] = six.moves.input(
                    'Provide {name}: '.format(name=name))
        return self._params


def create_config_symlink(installation, config_local_path):
    with chdir(installation.home_path):
        if os.path.exists(config_local_path):
            os.unlink(config_local_path)
        os.symlink(
            os.path.join(installation.files_path, config_local_path),
            config_local_path,
        )


def copy_config_template(installation, config_local_path, param_names=[],
                         **params):
    cfg_template_path = os.path.join(installation.files_path,
                                     config_local_path + '.j2')
    cfg_path = os.path.join(installation.home_path, config_local_path)
    if os.path.exists(cfg_path):
        os.unlink(cfg_path)
    with open(cfg_template_path, 'rt') as f:
        cfg_template = jinja2.Template(f.read())
    with open(cfg_path, 'wt') as f:
        template_params = {}
        template_params.update(installation.get_params(param_names))
        template_params.update(params)
        f.write(cfg_template.render(**template_params))
