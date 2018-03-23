import pathlib

import totoast.settings


def test_loadpath(datadir):
    a_b = totoast.settings.loadpath(datadir / 'a_b.toml')
    assert a_b == {'a': 'b'}

    empty = totoast.settings.loadpath(datadir / 'does_not_exist.toml')
    assert empty == {}


def test_loadexp(mocker):
    mocker.patch('totoast.settings.loadpath')
    path_home = pathlib.Path.home() / 'abcd'
    totoast.settings.loadexp(path_home)
    totoast.settings.loadpath.assert_called_once_with(path_home.expanduser())


def test_get_options(datadir):
    paths = [
        datadir / 'get_options1.toml',
        datadir / 'get_options2.toml'
    ]
    defaults = {
        'a': 10,
        'b': 20,
        'c': 30,
        'd': 40
    }
    results = {
        'a': 1,
        'b': 3,
        'c': 4,
        'd': 40
    }

    out = totoast.settings.get_options(defaults, paths)
    assert out == results
