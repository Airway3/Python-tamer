import importlib
import os
import random


class ChoicesHelper:
    @classmethod
    def make(cls, iterable):
        return tuple((item[0], item[1],) for item in iterable)

    @classmethod
    def make_from_dict(cls, d):
        return tuple((k, d[k],) for k in d)

    @classmethod
    def get_value(cls, iterable, key):
        for item in iterable:
            if len(item) > 1 and item[0] == key:
                return item[1]
        return None

    @classmethod
    def get_extra(cls, iterable, key):
        for item in iterable:
            if len(item) > 2 and item[0] == key:
                return item[2]
        return {}


def get_random_bool():
    return bool(random.getrandbits(1))


class clearable_file(object):
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        return self.filename

    def __exit__(self, type, value, traceback):
        if os.path.isfile(self.filename):
            os.remove(self.filename)


def import_by_name(name, module):
    """ Импорт по имени
    :param name: имя
    :return:
    """
    try:
        mod = importlib.import_module(module)
        return getattr(mod, name, None)
    except (ImportError, ImportWarning,):
        return None