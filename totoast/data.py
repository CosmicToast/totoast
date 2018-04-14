import enum


class EntryType(enum.Enum):
    Entry = 'Entry'
    List = 'List'


class Entry:

    def __init__(self, data, metadata='', etype='Entry'):
        self.data = data
        self.metadata = metadata
        self.type = EntryType(etype)

    def __iter__(self):
        yield 'data', self.data
        yield 'metadata', self.metadata
        yield 'type', self.type.value

    @staticmethod
    def load(json):
        return __class__(json['data'], json['metadata'], json['type'])


class ListMeta(type):

    def __new__(cls, name, bases, dct):
        instance = super().__new__(cls, name, bases, dct)
        instance.lists = {}
        return instance

    def __getitem__(self, key):
        if key in self.lists:
            return self.lists[key]
        else:
            self.lists[key] = self()
            return self[key]


class List(metaclass=ListMeta):

    # not meant to be explicitly initialized, so just setting available vars
    def __init__(self):
        self.entries = []
        self.parent = None  # Default
        self.loaded = False

    def __iter__(self):
        for entry in self.entries:
            yield dict(entry)

    # populate from json data
    def load(self, struct, parent='Default'):
        if self.loaded:
            return
        self.parent = parent
        for entry in struct:
            self.entries.append(Entry.load(entry))
        self.loaded = True
