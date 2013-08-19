#!/usr/bin/env python
from installhelpers.sublime_text import configure as sublime_text_configure
from installhelpers.vim import configure as vim_configure


def main():
    sublime_text_configure()
    vim_configure()

if __name__ == '__main__':
    main()
