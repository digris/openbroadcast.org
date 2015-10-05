# -*- coding: utf-8 -*-
VERSION = (0, 1, 2, 'final')

if VERSION[-1] != "final": # pragma: no cover
    __version__ = '.'.join(map(str, VERSION))
else: # pragma: no cover
    __version__ = '.'.join(map(str, VERSION[:-1]))
