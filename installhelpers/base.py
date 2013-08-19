import json
import os


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
    print(u'>>> {text}'.format(text=text))


def print_info(text):
    print(u'    {text}'.format(text=text))


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
