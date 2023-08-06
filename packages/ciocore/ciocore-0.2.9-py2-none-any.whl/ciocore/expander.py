
import os
import re
from string import Template


class AngleBracketTemplate(Template):
    """ Template for substituting tokens in angle brackets.

    Tokens may have mixed case letters and underscores.
    E.g. <foo>, <foo_bar> or <Scene>
    """
    delimiter = '<'
    pattern = r"""
        \<(?:
        (?P<escaped>\<)|
        (?P<named>  )\>|
        (?P<braced>[A-Za-z][A-Za-z_]+)\>|
        (?P<invalid>)
        )
        """


class Expander(object):
    """Class to expand angle bracket tokens."""

    def __init__(self,safe=False, **context):
        self.context = context
        self._safe = safe

    def evaluate(self, target):
        """Evaluate target, whether its a value, list, or dict."""
        if type(target) == dict:
            result = {}
            for k in target:
                result[k] = self.evaluate_item(target[k])
            return result
        elif type(target) == list:
            return [self.evaluate_item(value) for value in target]
        return self.evaluate_item(target)

    def evaluate_item(self, item):
        """Evaluate an expression string

        Replace <token>s with values provided by the context dict
        """
        item = os.path.expandvars(item.strip())
        if self._safe:
            return AngleBracketTemplate(item).safe_substitute(self.context)
        try:
            return AngleBracketTemplate(item).substitute(self.context)
        except KeyError:
                raise KeyError("Invalid token. Valid tokens are: {}".format(
                    self.context.keys()))

 