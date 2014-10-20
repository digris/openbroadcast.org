# work around modules with the same name
from __future__ import absolute_import

from debug_toolbar.utils.tracking import replace_call

from debug_toolbar_memcache.panels import BasePanel, record
import logging

DEBUG = False

logger = logging.getLogger(__name__)
try:
    import memcache as memc

    tracked_methods = [
        'flush_all',
        'delete_multi',
        'delete',
        'incr',
        'decr',
        'add',
        'append',
        'prepend',
        'replace',
        'set',
        'cas',
        'set_multi',
        'get',
        'gets',
        'get_multi',
    ]

    for m in tracked_methods:
        replace_call(getattr(memc.Client, m))(record)

except:
    if DEBUG:
        logger.exception('unable to install memcache.Client with tracking')
    else:
        logger.debug('unable to install memcache.Client with tracking')

MemcachePanel = BasePanel
