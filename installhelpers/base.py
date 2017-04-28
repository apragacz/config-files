from __future__ import print_function, unicode_literals, division
import contextlib
import datetime
import json
import os
import shutil

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
        json.dump(config, f, sort_keys=True, indent=2)


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

    def __init__(self, home_path, repo_path, params=None):
        if params is None:
            params = {}
        self.home_path = home_path
        self.repo_path = repo_path
        self.start_time = datetime.datetime.now()
        self._params = {}
        self._params.update(params)

    @property
    def files_path(self):
        return os.path.join(self.repo_path, 'files')

    @property
    def params_path(self):
        return os.path.join(self.repo_path, '.params.json')

    def _load_saved_params(self):
        try:
            with open(self.params_path, 'r') as f:
                return json.load(f)
        except IOError:
            return {}

    def _save_params(self, params):
        with open(self.params_path, 'w') as f:
            json.dump(params, f)

    def ask_for_params(self, required_names):
        saved_params = self._load_saved_params()
        for name in required_names:
            if name in self._params:
                continue
            value = ''
            while value == '':
                saved_value = saved_params.get(name)
                prompt_fmt = 'Provide {name}[{saved_value}]: ' if saved_value is not None else 'Provide {name}: '
                prompt = prompt_fmt.format(
                    name=name,
                    saved_value=saved_value,
                )
                value = six.moves.input(prompt)
                if not value and saved_value is not None:
                    value = saved_value
            self._params[name] = value

    def get_params(self, required_names):
        for name in required_names:
            if name not in self._params:
                raise ValueError("No '{name}' in params".format(name=name))
        return self._params

    def tear_down(self):
        self._save_params(self._params)


def create_config_symlink(installation, config_local_path):
    with chdir(installation.home_path):
        if os.path.exists(config_local_path):
            backup(installation, config_local_path, will_be_replaced=True)
        os.symlink(
            os.path.join(installation.files_path, config_local_path),
            config_local_path,
        )


def copy_config_template(installation, config_local_path, param_names=[],
                         **params):
    cfg_template_path = os.path.join(installation.files_path,
                                     config_local_path + '.j2')
    cfg_path = os.path.join(installation.home_path, config_local_path)
    with open(cfg_template_path, 'rt') as f:
        cfg_template = jinja2.Template(f.read())
    template_params = {}
    template_params.update(installation.get_params(param_names))
    template_params.update(params)
    config_content = cfg_template.render(**template_params)

    if os.path.exists(cfg_path):
        backup(installation, cfg_path, will_be_replaced=True)
    with open(cfg_path, 'wt') as f:
        f.write(config_content)


def append_config_line(installation, config_local_path, config_line,
                       if_line_not_exists=True):
    if '\n' in config_line:
        raise ValueError('Newline found in {line!r}'.format(config_line=config_line))
    cfg_path = os.path.join(installation.home_path, config_local_path)
    if not os.path.exists(cfg_path):
        return
    with open(cfg_path, 'rt') as f:
        cfg_lines = [line.strip() for line in f]
    if if_line_not_exists and config_line in cfg_lines:
        return
    backup(installation, cfg_path)
    with open(cfg_path, 'at') as f:
        f.write(config_line)
        f.write('\n')


def backup(installation, path, will_be_replaced=False):
    if os.path.islink(path):
        if will_be_replaced:
            os.unlink(path)
        return
    time_suffix = installation.start_time.strftime('%Y-%m-%d_%H-%M-%S')
    new_path = '{path}.{time_suffix}.old'.format(path=path, time_suffix=time_suffix)
    if will_be_replaced:
        os.rename(path, new_path)
    else:
        shutil.copy(path, new_path)
