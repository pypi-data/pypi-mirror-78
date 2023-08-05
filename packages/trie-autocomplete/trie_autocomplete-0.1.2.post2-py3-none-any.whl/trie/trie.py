class Trie:
    __slots__ = ('v', 'root', 'd', 'zero_complete')
    EMPTY = object()

    def __init__(self, *, zero_complete=True):
        self.d = {}
        self.root = True
        self.v = self.EMPTY
        self.zero_complete = zero_complete

    @classmethod
    def _create_item(cls, root=False):
        obj = cls()
        obj.root = root
        return obj

    def __getitem__(self, key):
        if len(key) == 0:
            if not self.is_set():
                raise KeyError(key.string)
            return self.v

        if key[0] not in self.d:
            raise KeyError(key.string)

        return self.d[key[0]][key[1:]]

    def __setitem__(self, key, value):
        if len(key) == 0:
            self.v = value
        else:
            if key[0] not in self.d:
                self.d[key[0]] = self._create_item(root=False)
            self.d[key[0]][key[1:]] = value

    def __delitem__(self, key):
        if len(key) == 0:
            if not self.is_set():
                raise KeyError(key.string)
            self.v = self.EMPTY
        else:
            if key[0] not in self.d:
                raise KeyError(key.string)
            del self.d[key[0]][key[1:]]
            if self.d[key[0]].empty():
                del self.d[key[0]]

    def empty(self):
        return len(self.d) == 0 and not self.is_set()

    def is_set(self):
        return self.v is not self.EMPTY

    def to_dict(self):
        d = {i + k: v for i, dct in self.d.items() for k, v in dct.items()}
        if self.is_set():
            d[''] = self.v
        return d

    def items(self):
        return self.to_dict().items()

    def keys(self):
        if self.is_set():
            yield ''
        for k, v in sorted(self.d.items()):
            for k1 in v.keys():
                yield k + k1

    def __contains__(self, key):
        try:
            self[key]
        except KeyError:
            return False
        return True

    def get_subtrie(self, key):
        if len(key) == 0:
            return self
        if key[0] not in self.d:
            raise KeyError(key.string)
        return self.d[key[0]].get_subtrie(key[1:])

    def complete(self, key):
        return self.get_subtrie(key).to_dict()

    def fix_typos(self, key, d=2, nadd=False, ndel=False):
        if len(key) == 0:
            if self.is_set():
                yield '', 0
            if not nadd:
                if self.zero_complete:
                    for k in self.keys():
                        yield k, 0
                else:
                    for k in self.keys():
                        if len(k) <= d:
                            yield k, len(k)
            return

        if key[0] in self.d:
            for tpl in self.d[key[0]].fix_typos(key[1:], d):
                yield (key[0] + tpl[0], tpl[1])

        if self.is_set() and len(key) <= d:
            yield '', len(key)

        if not nadd and d:
            # add
            for k in sorted(self.d.keys()):
                if k != key[0]:
                    for tpl in self.d[k].fix_typos(key, d - 1, ndel=True):
                        yield (k + tpl[0], tpl[1] + 1)
        if d:
            # change
            for k in sorted(self.d.keys()):
                if k != key[0]:
                    for tpl in self.d[k].fix_typos(key[1:], d - 1):
                        yield (k + tpl[0], tpl[1] + 1)
        if d and not ndel:
            # delete
            for tpl in self.fix_typos(key[1:], d - 1, nadd=True):
                yield (tpl[0], tpl[1] + 1)

    def autocomplete(self, key, *, maxd=2, limit=5):
        res = []
        for i in range(maxd + 1):
            for k, dst in self.fix_typos(key, i):
                if k not in res:
                    res.append(k)
                if len(res) == limit:
                    break
            if res:
                break
        return res
