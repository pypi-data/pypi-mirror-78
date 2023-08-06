import abc
import importlib
import inspect
import re


def split_camel(name):
    return re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', name)

class ValidationError(Exception):
    pass
 

class Validator(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, submitter):
        self._submitter = submitter
        self.errors = set()
        self.warnings = set()
        self.notices = set()

    def add_error(self, msg):
        self.errors.add("[{}]:\n{}".format(self.title(), msg))

    def add_warning(self, msg):
        self.warnings.add("[{}]:\n{}".format(self.title(), msg))

    def add_notice(self, msg):
        self.notices.add("[{}]:\n{}".format(self.title(), msg))

    @abc.abstractmethod
    def run(self, layername):
        return

    @classmethod
    def all_subclasses(cls):
        return set(cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in c.all_subclasses()]
        )

    @classmethod
    def plugins(cls):
        return [c for c in cls.all_subclasses() if not inspect.isabstract(c)]

    @classmethod
    def title(cls):
        return split_camel(cls.__name__)
