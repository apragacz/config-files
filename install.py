#!/usr/bin/env python
from __future__ import print_function
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
    try:
        homedir_path = os.environ['HOME']
        installation = Installation(
            homedir_path,
            os.path.join(homedir_path, 'config-files'),
        )
        modules_to_configure = []
        for module in MODULES:
            if not installation.prepare_with_module(module):
                continue
            modules_to_configure.append(module)

        installation.set_up()

        for module in modules_to_configure:
            module.configure(installation)

        installation.tear_down()
    except KeyboardInterrupt:
        print("\nInterrupted by user, quitting!")


if __name__ == '__main__':
    main()
