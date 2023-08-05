"""
XLate class multi regex substitution using a dictionary

Returns:
    str: text with any successful substitution
"""

import re


class XLate(dict):
    """ All-in-one multiple-string-substitution class """

    def _makeRegex(self):
        """ Build re object based on the keys of the current dictionary """
        return re.compile("|".join(map(re.escape, self.keys())))

    def __call__(self, match):
        """ Handler invoked for each regex match """
        return self[match.group(0)]

    def xLate(self, text):
        """ Translate text, returns the modified text. """
        return self._makeRegex().sub(self, text)
