#!/bin/bash

readonly VENV_DIR="$HOME/.install-venv"

main() {
  if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
  fi

  source "$VENV_DIR/bin/activate"

  pip install --upgrade pip
  pip install --upgrade wheel
  pip install --upgrade setuptools
  pip install jinja2

  python -m installer "$@"
}

main "$@"