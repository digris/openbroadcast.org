# -*- coding: utf-8 -*-
from __future__ import print_function
from collections import defaultdict
from . import mapping


def none_factory():
    return None


default_translate_table = defaultdict(none_factory, mapping.translate_table)


def fold(unicode_string, replacement=u''):
    """Fold unicode_string to ASCII.

Unmapped characters should be replaced with empty string by default, or other
replacement if provided.

All astral plane characters are always removed, even if a replacement is
provided.
    """

    if unicode_string is None:
        return u''

    if type(unicode_string) != unicode:
        raise TypeError('cannot fold bytestring')

    if type(replacement) != unicode:
        raise TypeError('cannot replace using bytestring')

    try:
        # If string contains only ASCII characters, just return it.
        unicode_string.decode('ascii')
        return unicode_string
    except (UnicodeDecodeError, UnicodeEncodeError) as ex:
        pass

    if replacement:
        def replacement_factory():
            return replacement

        translate_table = defaultdict(replacement_factory,
                                      mapping.translate_table)
    else:
        translate_table = default_translate_table

    return unicode_string.translate(translate_table)
