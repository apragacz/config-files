#!/usr/bin/env python
import os

from installhelpers.base import Installation
from installhelpers import (
    bash,
    git,
    tmux,
    vim,
    python_cli_tools,
)


def main():
    homedir_path = os.environ['HOME']
    installation = Installation(
        homedir_path,
        os.path.join(homedir_path, 'config-files'),
    )
    modules = [bash, git, tmux, vim, python_cli_tools]
    for module in modules:
        ask_for_params = getattr(module, 'ask_for_params', None)
        if not ask_for_params:
            continue
        ask_for_params(installation)
    for module in modules:
        module.configure(installation)

    installation.tear_down()


if __name__ == '__main__':
    main()
