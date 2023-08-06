class OneToManyInvertibleMapping(dict):
    class ReverseDict(dict):
        def __init__(self, obverse, *args, **kwargs):
            self._obverse = obverse
            self._base = super()
            super().__init__(*args, **kwargs)

        @property
        def obverse(self):
            return self._obverse

        def __setitem__(self, key, value):
            if super().__contains__(key):
                if super().__getitem__(key) is value:
                    return

                raise ValueError('value is already obversely mapped to a different key - '
                                 'if you want to reset the relation, first delete key from value in the obverse '
                                 'mapping')

            super().__setitem__(key, value)

            if self._obverse._base.__contains__(value):
                obverse_set = self._obverse.__getitem__(value)
            else:
                obverse_set = set()
                self._obverse._base.__setitem__(value, obverse_set)

            obverse_set.add(key)

        def __delitem__(self, key):
            value = super().__getitem__(key)
            super().__delitem__(key)

            obverse_set = self._obverse._base.__getitem__(value)
            obverse_set.remove(key)
            if not obverse_set:
                self._obverse._base.__delitem__(value)

    def __init__(self, *args, **kwargs):
        self._reverse = self.ReverseDict(self)
        self._base = super()
        super().__init__(*args, **kwargs)

    @property
    def reverse(self):
        return self._reverse

    def __setitem__(self, key, value):
        if super().__contains__(key):
            obverse_set = super().__getitem__(key)
        else:
            obverse_set = set()
            super().__setitem__(key, obverse_set)

        obverse_set.add(value)

        self._reverse._base.__setitem__(value, key)

    def __delitem__(self, key):
        obverse_set = super().__getitem__(key)
        super().__delitem__(key)

        for reverse in obverse_set:
            self._reverse._base.__delitem__(reverse)
