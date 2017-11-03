#!/usr/bin/env python
import os

from installhelpers.installation import Installation
from installhelpers import (
    bash,
    git,
    python_cli_tools,
    tmux,
    vim,
    vscode,
)

MODULES = (
    bash,
    git,
    tmux,
    vim,
    vscode,
    python_cli_tools,
)


def main():
    homedir_path = os.environ['HOME']
    installation = Installation(
        homedir_path,
        os.path.join(homedir_path, 'config-files'),
    )
    for module in MODULES:
        installation.prepare_with_module(module)

    installation.set_up()

    for module in MODULES:
        module.configure(installation)

    installation.tear_down()


if __name__ == '__main__':
    main()
