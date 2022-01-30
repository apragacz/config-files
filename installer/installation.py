import datetime
import json
import os
import platform


PATH_OS_REMAPS = {
    'darwin': {
        '.config/Code': 'Library/Application Support/Code'
    }
}


class Installation(object):

    def __init__(self, home_path, repo_path, params=None):
        if params is None:
            params = {}
        self.home_path = home_path
        self.repo_path = repo_path
        self.start_time = datetime.datetime.now()
        self._required_param_names = set()
        self._params = {}
        self._params.update(params)

    @property
    def os_name(self):
        return platform.system().lower()

    @property
    def path_sep(self):
        return os.path.sep

    @property
    def files_path(self):
        return os.path.join(self.repo_path, 'files')

    @property
    def params_path(self):
        return os.path.join(self.repo_path, '.params.json')

    def remap_home_path(self, local_path):
        sep = self.path_sep
        path = local_path
        path_remaps = PATH_OS_REMAPS.get(self.os_name, {})
        for src_prefix, dst_prefix in path_remaps.items():
            if not src_prefix.endswith(sep) and not dst_prefix.endswith(sep):
                src_prefix += sep
                dst_prefix += sep
            if path.startswith(src_prefix):
                path = dst_prefix + path[len(src_prefix):]
        return path

    def get_home_abspath(self, local_path):
        return os.path.join(self.home_path, self.remap_home_path(local_path))

    def _load_saved_params(self):
        try:
            with open(self.params_path, 'r') as f:
                return json.load(f)
        except IOError:
            return {}

    def _save_params(self, params):
        with open(self.params_path, 'w') as f:
            json.dump(params, f)

    @staticmethod
    def _get_input_prompt(name, saved_value=None):
        if saved_value is not None:
            prompt_fmt = 'Provide {name} [{saved_value}]: '
        else:
            prompt_fmt = 'Provide {name}: '
        prompt = prompt_fmt.format(
            name=name,
            saved_value=saved_value,
        )
        return prompt

    def prepare_with_module(self, module):
        prepare = getattr(module, 'prepare', None)
        if not prepare:
            return True
        result = prepare(self)  # pylint: disable=E1102

        configure = getattr(module, 'configure', None)
        if configure is None:
            raise AttributeError(
                'No configure function in module {module!r}'.format(
                    module=module))

        return not (result is False)

    def require_params(self, param_names):
        self._required_param_names.update(param_names)

    def _ask_for_params(self):
        required_names = sorted(self._required_param_names)
        saved_params = self._load_saved_params()
        for name in required_names:
            if name in self._params:
                continue
            value = ''
            while value == '':
                saved_value = saved_params.get(name)
                prompt = self._get_input_prompt(name, saved_value=saved_value)
                value = input(prompt)
                if not value and saved_value is not None:
                    value = saved_value
            self._params[name] = value

    def _confirm_params(self):
        required_names = sorted(self._required_param_names)
        print("Params:")
        for name in required_names:
            value = self._params[name]
            print("  {name}: {value}".format(name=name, value=value))
        confirm = input("Are these ok? [y/N]: ")
        if confirm.lower() != 'y':
            raise KeyboardInterrupt()

    def get_params(self, required_names):
        for name in required_names:
            if name not in self._params:
                raise ValueError("No '{name}' in params".format(name=name))
        return self._params

    def set_up(self):
        print(vars(self))
        self._ask_for_params()
        self._confirm_params()

    def tear_down(self):
        self._save_params(self._params)
