# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from cacheops import cache
from cacheops.cross import md5hex


def uuid_func_cache_key(func, args, kwargs, extra=None):
    """
    Calculate cache key based on func and arguments,
    additionally appending uuids to factors if present.
    The built-in cached decorator uses the __unicode__ of an instance when building
    the factors. This leads to non-unique cache in case of same __unicode__ value.
    (e.g. having the same "name" in different objects)
    """

    factors = [func.__module__, func.__name__, args, kwargs, extra]
    if hasattr(func, "__code__"):
        factors.append(func.__code__.co_firstlineno)

    for arg in args:
        if hasattr(arg, "uuid"):
            factors.append(arg.uuid)

    return md5hex(json.dumps(factors, sort_keys=True, default=str))


def cached_uuid_aware(timeout=None, extra=None, key_func=uuid_func_cache_key):
    """
    uuid aware version of cacheops 'cached'
    """
    return cache.cached(timeout=None, extra=None, key_func=uuid_func_cache_key)
