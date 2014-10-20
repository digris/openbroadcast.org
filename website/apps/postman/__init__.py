"""
A messaging application for Django
"""
from __future__ import unicode_literals

# following PEP 386: N.N[.N]+[{a|b|c|rc}N[.N]+][.postN][.devN]
VERSION = (2, 2, 0)
PREREL = ('a', 1)
POST = 0
DEV = 0


def get_version():
    version = '.'.join(map(str, VERSION))
    if PREREL:
        version += PREREL[0] + '.'.join(map(str, PREREL[1:]))
    if POST:
        version += ".post" + str(POST)
    if DEV:
        version += ".dev" + str(DEV)
    return version

__version__ = get_version()
