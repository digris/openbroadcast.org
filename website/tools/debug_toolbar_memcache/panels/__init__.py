# work around modules with the same name
from __future__ import absolute_import

from datetime import datetime
import logging
from os.path import dirname, realpath
import sys

from debug_toolbar.middleware import DebugToolbarMiddleware
from debug_toolbar.panels import DebugPanel
from debug_toolbar.utils import tidy_stacktrace, get_stack, ms_from_timedelta, get_template_info
from django.conf import settings
from django.template import Node
from django.template.loader import render_to_string
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

# Get config vars

toolbar_config = getattr(settings, 'DEBUG_TOOLBAR_CONFIG', {})
ENABLE_STACKTRACES = toolbar_config.get('ENABLE_STACKTRACES', True)

logger = logging.getLogger(__name__)

def record(func, *args, **kwargs):
    djdt = DebugToolbarMiddleware.get_current()
    if not djdt:
        return func(*args, **kwargs)

    panel = djdt.get_panel(BasePanel)

    # Get stacktrace
    if ENABLE_STACKTRACES:
        stacktrace = tidy_stacktrace(reversed(get_stack()))
    else:
        stacktrace = []

    # Get template info
    template_info = None
    cur_frame = sys._getframe().f_back
    try:
        while cur_frame is not None:
            if cur_frame.f_code.co_name == 'render':
                node = cur_frame.f_locals['self']
                if isinstance(node, Node):
                    template_info = get_template_info(node.source)
                    break
            cur_frame = cur_frame.f_back
    except:
        pass
    del cur_frame

    # Find args
    cache_args = None
    # first arg is self, do we have another
    if len(args) > 1:
        cache_args = args[1]
        # is it a dictionary (most likely multi)
        if isinstance(cache_args, dict):
            # just use it's keys
            cache_args = cache_args.keys()

    # the clock starts now
    start = datetime.now()
    try:
        return func(*args, **kwargs)
    finally:
        # the clock stops now
        duration = ms_from_timedelta(datetime.now() - start)
        call = {
            'function': func.__name__,
            'args': cache_args,
            'duration': duration,
            'stacktrace': stacktrace,
            'template_info': template_info,
        }
        panel.record(**call)



class BasePanel(DebugPanel):
    name = 'Memcache'
    has_content = True

    def __init__(self, *args, **kwargs):
        super(BasePanel, self).__init__(*args, **kwargs)
        self._cache_time = 0
        self._num_calls = 0
        self._calls = []

    def record(self, **call):
        self._cache_time += call['duration']
        self._num_calls += 1
        self._calls.append(call)

    def nav_title(self):
        return _('Memcache')

    def nav_subtitle(self):
        return "%d %s in %.2fms" % (
            self._num_calls,
            (self._num_calls == 1) and 'call' or 'calls',
            self._cache_time
            )

    def title(self):
        return _('Memcache Calls')

    def url(self):
        return ''

    def content(self):
        calls = self._calls

        for call in calls:
            stacktrace = []
            for frame in call['stacktrace']:
                params = map(escape, frame[0].rsplit('/', 1) + list(frame[1:]))
                try:
                    stacktrace.append(u'<span class="path">{0}/</span><span class="file">{1}</span> in <span class="func">{3}</span>(<span class="lineno">{2}</span>)\n  <span class="code">{4}</span>'.format(*params))
                except IndexError:
                    # This frame doesn't have the expected format, so skip it and move on to the next one
                    continue
            call['stacktrace'] = mark_safe('\n'.join(stacktrace))

        context = self.context.copy()
        context.update({
            'calls': calls,
            'count': len(calls),
            'duration': self._cache_time,
        })

        return render_to_string('memcache_toolbar/panels/memcache.html',
                context)
