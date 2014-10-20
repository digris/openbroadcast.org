"""
If the default usage of the views suits you, simply use a line like
this one in your root URLconf to set up the default URLs::

    (r'^messages/', include('postman.urls')),

Otherwise you may customize the behavior by passing extra parameters.

Recipients Max
--------------
Views supporting the parameter are: ``write``, ``reply``.
Example::
    ..., {'max': 3}, name='postman_write'),
See also the ``POSTMAN_DISALLOW_MULTIRECIPIENTS`` setting

User filter
-----------
Views supporting a user filter are: ``write``, ``reply``.
Example::
    def my_user_filter(user):
        if user.get_profile().is_absent:
            return "is away"
        return None
    ...
    ..., {'user_filter': my_user_filter}, name='postman_write'),

function interface:
In: a User instance
Out: None, False, '', 'a reason', or ValidationError

Exchange filter
---------------
Views supporting an exchange filter are: ``write``, ``reply``.
Example::
    def my_exchange_filter(sender, recipient, recipients_list):
        if recipient.relationships.exists(sender, RelationshipStatus.objects.blocking()):
            return "has blacklisted you"
        return None
    ...
    ..., {'exchange_filter': my_exchange_filter}, name='postman_write'),

function interface:
In:
    ``sender``: a User instance
    ``recipient``: a User instance
    ``recipients_list``: the full list of recipients
Out: None, False, '', 'a reason', or ValidationError

Auto-complete field
-------------------
Views supporting an auto-complete parameter are: ``write``, ``reply``.
Examples::
    ..., {'autocomplete_channels': (None,'anonymous_ac')}, name='postman_write'),
    ..., {'autocomplete_channels': 'write_ac'}, name='postman_write'),
    ..., {'autocomplete_channel': 'reply_ac'}, name='postman_reply'),

Auto moderators
---------------
Views supporting an ``auto-moderators`` parameter are: ``write``, ``reply``.
Example::
    def mod1(message):
        # ...
        return None
    def mod2(message):
        # ...
        return None
    mod2.default_reason = 'mod2 default reason'
    ...
    ..., {'auto_moderators': (mod1, mod2)}, name='postman_write'),
    ..., {'auto_moderators': mod1}, name='postman_reply'),

function interface:
In: ``message``: a Message instance
Out: rating or (rating, "reason")
    with reting: None, 0 or False, 100 or True, 1..99

Others
------
Refer to documentation.
    ..., {'form_classes': (MyCustomWriteForm, MyCustomAnonymousWriteForm)}, name='postman_write'),
    ..., {'form_class': MyCustomFullReplyForm}, name='postman_reply'),
    ..., {'form_class': MyCustomQuickReplyForm}, name='postman_view'),
    ..., {'template_name': 'my_custom_view.html'}, name='postman_view'),
    ..., {'success_url': 'postman_inbox'}, name='postman_reply'),
    ..., {'formatters': (format_subject,format_body)}, name='postman_reply'),
    ..., {'formatters': (format_subject,format_body)}, name='postman_view'),

"""
from __future__ import unicode_literals

try:
    from django.conf.urls import patterns, include, url  # django 1.4
except ImportError:
    from django.conf.urls.defaults import patterns, include, url  # django 1.3
from django.views.generic.base import RedirectView

OPTION_MESSAGES = 'm'
OPTIONS = OPTION_MESSAGES

urlpatterns = patterns('postman.views',
    url(r'^inbox/(?:(?P<option>'+OPTIONS+')/)?$', 'inbox', name='postman_inbox'),
    url(r'^sent/(?:(?P<option>'+OPTIONS+')/)?$', 'sent', name='postman_sent'),
    url(r'^archives/(?:(?P<option>'+OPTIONS+')/)?$', 'archives', name='postman_archives'),
    url(r'^trash/(?:(?P<option>'+OPTIONS+')/)?$', 'trash', name='postman_trash'),
    url(r'^write/(?:(?P<recipients>[\w.@+-:]+)/)?$', 'write', name='postman_write'),
    url(r'^reply/(?P<message_id>[\d]+)/$', 'reply', name='postman_reply'),
    url(r'^view/(?P<message_id>[\d]+)/$', 'view', name='postman_view'),
    url(r'^view/t/(?P<thread_id>[\d]+)/$', 'view_conversation', name='postman_view_conversation'),
    url(r'^archive/$', 'archive', name='postman_archive'),
    url(r'^delete/$', 'delete', name='postman_delete'),
    url(r'^undelete/$', 'undelete', name='postman_undelete'),
    (r'^$', RedirectView.as_view(url='inbox/')),
)
