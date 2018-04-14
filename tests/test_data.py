import json
import pytest

import totoast.data


def test_entrytype():
    entry = totoast.data.EntryType('Entry')
    lst = totoast.data.EntryType('List')

    assert entry != lst
    assert entry.value == 'Entry'
    assert lst.value == 'List'

    with pytest.raises(ValueError, match=r'.* is not a valid EntryType'):
        wrong = totoast.data.EntryType('Wrong')


class TestEntry():
    ent = totoast.data.Entry('data', 'metadata', 'List')
    dfl = totoast.data.Entry('data')

    tl = totoast.data.EntryType('List')
    te = totoast.data.EntryType('Entry')

    jl = '''{
    "data": "data",
    "metadata": "metadata",
    "type": "List"
}'''
    je = '''{
    "data": "data",
    "metadata": "",
    "type": "Entry"
}'''

    def test_init(self):
        assert __class__.ent.data == 'data'
        assert __class__.ent.metadata == 'metadata'
        assert __class__.ent.type == __class__.tl

        assert __class__.dfl.data == 'data'
        assert __class__.dfl.metadata == ''
        assert __class__.dfl.type == __class__.te

    def test_iter(self):
        een = {'data': 'data', 'metadata': 'metadata', 'type': 'List'}
        edf = {'data': 'data', 'metadata': '', 'type': 'Entry'}

        assert dict(__class__.ent) == een
        assert dict(__class__.dfl) == edf

    def test_load(self):
        jdl = json.loads(__class__.jl)
        jde = json.loads(__class__.je)

        jnt = totoast.data.Entry.load(jdl)
        jfl = totoast.data.Entry.load(jde)

        assert dict(jnt) == dict(__class__.ent)
        assert dict(jfl) == dict(__class__.dfl)

        assert json.dumps(dict(__class__.ent), indent=4) == __class__.jl
        assert json.dumps(dict(__class__.dfl), indent=4) == __class__.je


class TestListMeta():
    class T(metaclass=totoast.data.ListMeta):
        pass

    def test_autoinit(self):
        __class__.T['autoinit']
        assert 'autoinit' in __class__.T.lists

    def test_persistence(self):
        __class__.T['persistence'].x = 2
        assert __class__.T['persistence'].x == 2


class TestList():
    e1 = totoast.data.Entry('data1', 'metadata1', 'Entry')
    e2 = totoast.data.Entry('data2', 'metadata2', 'List')

    jt = '''[
    {"data": "data1", "metadata": "metadata1", "type": "Entry"},
    {"data": "data2", "metadata": "metadata2", "type": "List"}
]'''

    def test_autoinit(self):
        assert totoast.data.List['autoinit'].entries == []

    def test_iter(self):
        totoast.data.List['iter'].load(json.loads(__class__.jt))
        res = totoast.data.List['iter']
        lrs = list(res)

        assert lrs == [dict(__class__.e1), dict(__class__.e2)]

    def test_load(self):
        totoast.data.List['load'].load(json.loads(__class__.jt))
        res = totoast.data.List['load']

        comp = totoast.data.List()
        comp.entries.append(__class__.e1)
        comp.entries.append(__class__.e2)
        comp.loaded = True

        assert res.parent == 'Default'
        assert list(res) == list(comp)

    def test_loaded(self):
        totoast.data.List['loaded'].load(json.loads(__class__.jt))
        totoast.data.List['reloaded'].load(json.loads(__class__.jt))
        totoast.data.List['reloaded'].load('')

        loaded = totoast.data.List['loaded']
        reloaded = totoast.data.List['reloaded']

        assert list(loaded) == list(reloaded)
