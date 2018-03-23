import os
import pathlib

import funcy
import toml

# temporary defaults - value will change
defaults = toml.loads(
    """
[config]
location = '~/.local/share/totoast'

[colors]
project = 'yellow'

"""
    )

confdir = (os.getenv('LOCALAPPDATA') or
           os.getenv('XDG_CONFIG_DIR') or
           '~/.config')
paths = [
    pathlib.Path(confdir) / 'totoast' / 'config.toml',
    pathlib.Path('~/.totoastrc')
]


def loadpath(p): return {} if not p.exists() else toml.loads(p.read_text())


def loadexp(p): return loadpath(p.expanduser())


def get_options(default, path):
    return funcy.join([default] + funcy.walk(loadexp, path))

options = get_options(defaults, paths)
