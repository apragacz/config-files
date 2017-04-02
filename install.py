#!/usr/bin/env python
import os

from installhelpers.base import Installation
from installhelpers import (
    vim,
    git,
    tmux,
)


def main():
    homedir_path = os.environ['HOME']
    installation = Installation(
        homedir_path,
        os.path.join(homedir_path, 'config-files'),
    )
    for module in [git, vim, tmux]:
        module.configure(installation)


if __name__ == '__main__':
    main()
