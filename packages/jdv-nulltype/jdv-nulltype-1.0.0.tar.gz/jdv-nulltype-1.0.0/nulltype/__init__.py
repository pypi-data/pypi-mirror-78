class SingletonMetatype(type):
    def __new__(self, name, bases, d):
        d["_instance"] = None
        d["__boo__"] = self.__bool__
        return type.__new__(SingletonMetatype, name, tuple(), d)

    def __init__(self, name, bases, d):
        name = name
        super().__init__(name, bases, d)

    def __call__(self):
        if self._instance is None:
            self._instance = SingletonMetatype.__new__(
                self.__class__, self.__name__, tuple(), {}
            )
        return self._instance

    def __bool__(self):
        return False


class _Null(metaclass=SingletonMetatype):
    pass


NullType = _Null

Null = NullType()
