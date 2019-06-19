from __future__ import print_function, unicode_literals, division
import contextlib
import json
import logging
import os
import shutil

import jinja2

logger = logging.getLogger(__name__)


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
    logger.info("Ensuring that path {dirpath!r} is created".format(
        dirpath=dirpath))
    if not (os.path.exists(dirpath) and os.path.isdir(dirpath)):
        logger.debug(
            "Directory path {dirpath!r} does not exist,"
            " creating required directories".format(dirpath=dirpath))
        os.makedirs(dirpath)


@contextlib.contextmanager
def chdir(dir_path):
    olddir_path = os.getcwd()
    os.chdir(dir_path)
    yield
    os.chdir(olddir_path)


def ensure_home_dirpath_created(installation, local_path):
    ensure_dirpath_created(installation.get_home_abspath(local_path))


def create_config_symlink(installation, config_local_path):
    home_config_local_path = installation.remap_home_path(config_local_path)
    with chdir(installation.home_path):
        if os.path.exists(home_config_local_path):
            backup(installation, home_config_local_path, will_be_replaced=True)
        os.symlink(
            os.path.join(installation.files_path, config_local_path),
            home_config_local_path,
        )
        return True


def copy_config_template(installation, config_local_path, param_names=None,
                         **params):
    if param_names is None:
        param_names = []
    cfg_template_path = os.path.join(installation.files_path,
                                     config_local_path + '.j2')
    cfg_path = installation.get_home_abspath(config_local_path)
    with open(cfg_template_path, 'rt') as f:
        cfg_template = jinja2.Template(f.read())
    template_params = {}
    template_params.update(installation.get_params(param_names))
    template_params.update(params)
    config_content = cfg_template.render(**template_params)

    if os.path.exists(cfg_path):
        with open(cfg_path, 'rt') as f:
            old_config_content = f.read()
            if config_content == old_config_content:
                logger.debug("New content of {cfg_path!r} is the same".format(
                    cfg_path=cfg_path))
                return False

    if os.path.exists(cfg_path):
        backup(installation, cfg_path, will_be_replaced=True)
    with open(cfg_path, 'wt') as f:
        f.write(config_content)
    return True


def append_config_line(installation, config_local_path, config_line,
                       if_line_not_exists=True):
    if '\n' in config_line:
        raise ValueError('Newline found in {config_line!r}'.format(
            config_line=config_line))
    cfg_path = installation.get_home_abspath(config_local_path)
    if os.path.exists(cfg_path):
        with open(cfg_path, 'rt') as f:
            cfg_lines = [line.strip() for line in f]
    else:
        cfg_lines = []
    if if_line_not_exists and config_line in cfg_lines:
        logger.debug("Line was already added to {cfg_path!r}".format(
            cfg_path=cfg_path))
        return False

    if os.path.exists(cfg_path):
        backup(installation, cfg_path)

    logger.info("Appending line to {cfg_path!r}".format(cfg_path=cfg_path))
    with open(cfg_path, 'at') as f:
        f.write(config_line)
        f.write('\n')
    return True


def backup(installation, path, will_be_replaced=False):
    if os.path.islink(path):
        if will_be_replaced:
            logging.debug("Removing link {path}".format(path=path))
            os.unlink(path)
        return False
    time_suffix = installation.start_time.strftime('%Y-%m-%d_%H-%M-%S')
    new_path = '{path}.{time_suffix}.old'.format(
        path=path,
        time_suffix=time_suffix)
    logger.info("Backing up {path!r}".format(path=path))
    if will_be_replaced:
        logger.debug("Moving {path!r} to {new_path!r}".format(
            path=path, new_path=new_path))
        os.rename(path, new_path)
    else:
        logger.debug("Copying {path!r} to {new_path!r}".format(
            path=path, new_path=new_path))
        shutil.copy(path, new_path)
    return True
