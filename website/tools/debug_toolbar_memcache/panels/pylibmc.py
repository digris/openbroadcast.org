# work around modules with the same name
from __future__ import absolute_import

from debug_toolbar.utils.tracking import replace_call

from debug_toolbar_memcache.panels import BasePanel, record
import logging

DEBUG = False

logger = logging.getLogger(__name__)
try:
    import pylibmc
    import _pylibmc

    tracked_methods = [
        'set',
        'set_multi',
        'get',
        'get_multi',
        'add',
        'replace',
        'append',
        'prepend',
        'incr',
        'decr',
        'delete',
        'delete_multi',
        'flush_all',
        ]

    for m in tracked_methods:
        replace_call(getattr(memc.Client, m))(record)

except:
    if DEBUG:
        logger.exception('unable to install pylibmc.Client with tracking')
    else:
        logger.debug('unable to install pylibmc.Client with tracking')


PylibmcPanel = BasePanel
