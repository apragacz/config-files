#!/usr/bin/env python
import os

from installhelpers.installation import Installation
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
        installation.prepare_with_module(module)

    installation.set_up()

    for module in modules:
        module.configure(installation)

    installation.tear_down()


if __name__ == '__main__':
    main()
