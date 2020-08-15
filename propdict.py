class PropDict(object):

    def __init__(self, value):
        self.value = value

    def __len__(self):
        return len(self.value)

    def __iter__(self):
        return map(PropDict, self.value)

    def __getattr__(self, name):
        return self[name]

    def __getitem__(self, key):
        try:
            return PropDict(self.value[key])
        except:
            return PropDict(None)

    def __str__(self):
        return str(self.value)

    def __format__(self, spec):
        if self.value is None:
            return "".__format__(spec)
        return self.value.__format__(spec)

    def toJSON(self):
        return json.dumps(self.value)
