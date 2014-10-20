from __future__ import unicode_literals
import urlparse

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
try:
    from django.contrib.auth import get_user_model  # Django 1.5
except ImportError:
    from postman.future_1_5 import get_user_model
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
try:
    from django.utils.timezone import now  # Django 1.4 aware datetimes
except ImportError:
    from datetime import datetime
    now = datetime.now

from postman.fields import autocompleter_app
from postman.forms import WriteForm, AnonymousWriteForm, QuickReplyForm, FullReplyForm
from postman.models import Message, get_order_by
from postman.urls import OPTION_MESSAGES
from postman.utils import format_subject, format_body


##########
# Helpers
##########
def _get_referer(request):
    """Return the HTTP_REFERER, if existing."""
    if 'HTTP_REFERER' in request.META:
        sr = urlparse.urlsplit(request.META['HTTP_REFERER'])
        return urlparse.urlunsplit(('', '', sr.path, sr.query, sr.fragment))


########
# Views
########
def _folder(request, folder_name, view_name, option, template_name):
    """Code common to the folders."""
    kwargs = {}
    if option:
        kwargs.update(option=option)
    order_by = get_order_by(request.GET)
    if order_by:
        kwargs.update(order_by=order_by)
    msgs = getattr(Message.objects, folder_name)(request.user, **kwargs)
    return render_to_response(template_name, {
        'pm_messages': msgs,  # avoid 'messages', already used by contrib.messages
        'by_conversation': option is None,
        'by_message': option == OPTION_MESSAGES,
        'by_conversation_url': reverse(view_name),
        'by_message_url': reverse(view_name, args=[OPTION_MESSAGES]),
        'current_url': request.get_full_path(),
        'gets': request.GET,  # useful to postman_order_by template tag
        }, context_instance=RequestContext(request))


@login_required
def inbox(request, option=None, template_name='postman/inbox.html'):
    """
    Display the list of received messages for the current user.

    Optional arguments:
        ``option``: display option:
            OPTION_MESSAGES to view all messages
            default to None to view only the last message for each conversation
        ``template_name``: the name of the template to use

    """
    return _folder(request, 'inbox', 'postman_inbox', option, template_name)


@login_required
def sent(request, option=None, template_name='postman/sent.html'):
    """
    Display the list of sent messages for the current user.

    Optional arguments: refer to inbox()

    """
    return _folder(request, 'sent', 'postman_sent', option, template_name)


@login_required
def archives(request, option=None, template_name='postman/archives.html'):
    """
    Display the list of archived messages for the current user.

    Optional arguments: refer to inbox()

    """
    return _folder(request, 'archives', 'postman_archives', option, template_name)


@login_required
def trash(request, option=None, template_name='postman/trash.html'):
    """
    Display the list of deleted messages for the current user.

    Optional arguments: refer to inbox()

    """
    return _folder(request, 'trash', 'postman_trash', option, template_name)


def write(request, recipients=None, form_classes=(WriteForm, AnonymousWriteForm), autocomplete_channels=None,
        template_name='postman/write.html', success_url=None,
        user_filter=None, exchange_filter=None, max=None, auto_moderators=[]):
    """
    Display a form to compose a message.

    Optional arguments:
        ``recipients``: a colon-separated list of usernames
        ``form_classes``: a 2-tuple of form classes
        ``autocomplete_channels``: a channel name or a 2-tuple of names
        ``template_name``: the name of the template to use
        ``success_url``: where to redirect to after a successful POST
        ``user_filter``: a filter for recipients
        ``exchange_filter``: a filter for exchanges between a sender and a recipient
        ``max``: an upper limit for the recipients number
        ``auto_moderators``: a list of auto-moderation functions

    """

    print '-- postmam write, to: -------'
    print recipients
    print '-----------------------------'


    user = request.user
    form_class = form_classes[0] if user.is_authenticated() else form_classes[1]
    if isinstance(autocomplete_channels, tuple) and len(autocomplete_channels) == 2:
        channel = autocomplete_channels[user.is_anonymous()]
    else:
        channel = autocomplete_channels
    next_url = _get_referer(request)
    if request.method == 'POST':

        print ' * request is post'

        form = form_class(request.POST, sender=user, channel=channel,
            user_filter=user_filter,
            exchange_filter=exchange_filter,
            max=max)

        if form.is_valid():
            print ' * form is valid trying to save'
            is_successful = form.save(auto_moderators=auto_moderators, hacked_recipient=recipients)
            print ' * form is post save'

            if is_successful:
                print ' * successfully saved message'
                messages.success(request, _("Message successfully sent."), fail_silently=False)
            else:
                print ' * message rejected'
                messages.warning(request, _("Message rejected for at least one recipient."), fail_silently=False)
            return redirect(request.GET.get('next', success_url or next_url or 'postman_inbox'))

        else:
            print ' * form is _not_ valid'


    else:
        initial = dict(request.GET.items())  # allow optional initializations by query string
        if recipients:
            # order_by() is not mandatory, but: a) it doesn't hurt; b) it eases the test suite
            # and anyway the original ordering cannot be respected.
            user_model = get_user_model()
            usernames = list(user_model.objects.values_list(user_model.USERNAME_FIELD, flat=True).filter(
                is_active=True,
                **{'{0}__in'.format(user_model.USERNAME_FIELD): [r.strip() for r in recipients.split(':') if r and not r.isspace()]}
            ).order_by(user_model.USERNAME_FIELD))
            if usernames:
                initial.update(recipients=', '.join(usernames))
        form = form_class(initial=initial, channel=channel)
    return render_to_response(template_name, {
        'form': form,
        'autocompleter_app': autocompleter_app,
        'next_url': request.GET.get('next', next_url),
        }, context_instance=RequestContext(request))
if getattr(settings, 'POSTMAN_DISALLOW_ANONYMOUS', False):
    write = login_required(write)


@login_required
def reply(request, message_id, form_class=FullReplyForm, formatters=(format_subject,format_body), autocomplete_channel=None,
        template_name='postman/reply.html', success_url=None,
        user_filter=None, exchange_filter=None, max=None, auto_moderators=[]):
    """
    Display a form to compose a reply.

    Optional arguments:
        ``form_class``: the form class to use
        ``formatters``: a 2-tuple of functions to prefill the subject and body fields
        ``autocomplete_channel``: a channel name
        ``template_name``: the name of the template to use
        ``success_url``: where to redirect to after a successful POST
        ``user_filter``: a filter for recipients
        ``exchange_filter``: a filter for exchanges between a sender and a recipient
        ``max``: an upper limit for the recipients number
        ``auto_moderators``: a list of auto-moderation functions

    """
    user = request.user
    perms = Message.objects.perms(user)
    parent = get_object_or_404(Message, perms, pk=message_id)
    initial = parent.quote(*formatters)
    next_url = _get_referer(request)
    if request.method == 'POST':
        post = request.POST.copy()
        if 'subject' not in post:  # case of the quick reply form
            post['subject'] = initial['subject']
        form = form_class(post, sender=user, recipient=parent.sender or parent.email,
            channel=autocomplete_channel,
            user_filter=user_filter,
            exchange_filter=exchange_filter,
            max=max)
        if form.is_valid():
            is_successful = form.save(parent=parent, auto_moderators=auto_moderators)
            if is_successful:
                messages.success(request, _("Message successfully sent."), fail_silently=True)
            else:
                messages.warning(request, _("Message rejected for at least one recipient."), fail_silently=True)
            return redirect(request.GET.get('next', success_url or next_url or 'postman_inbox'))
    else:
        initial.update(request.GET.items())  # allow overwriting of the defaults by query string
        form = form_class(initial=initial, channel=autocomplete_channel)
    return render_to_response(template_name, {
        'form': form,
        'recipient': parent.obfuscated_sender,
        'autocompleter_app': autocompleter_app,
        'next_url': request.GET.get('next', next_url),
        }, context_instance=RequestContext(request))


def _view(request, filter, form_class=QuickReplyForm, formatters=(format_subject,format_body),
        template_name='postman/view.html'):
    """
    Code common to the by-message and by-conversation views.

    Optional arguments:
        ``form_class``: the form class to use
        ``formatters``: a 2-tuple of functions to prefill the subject and body fields
        ``template_name``: the name of the template to use

    """
    user = request.user
    msgs = Message.objects.thread(user, filter)
    if msgs:
        Message.objects.set_read(user, filter)
        # are all messages archived ?
        for m in msgs:
            if not getattr(m, ('sender' if m.sender == user else 'recipient') + '_archived'):
                archived = False
                break
        else:
            archived = True
        # look for the more recent received message (and non-deleted to comply with the future perms() control), if any
        for m in reversed(msgs):
            if m.recipient == user and not m.recipient_deleted_at:
                received = m
                break
        else:
            received = None
        return render_to_response(template_name, {
            'pm_messages': msgs,
            'archived': archived,
            'reply_to_pk': received.pk if received else None,
            'form': form_class(initial=received.quote(*formatters)) if received else None,
            'next_url': request.GET.get('next', reverse('postman_inbox')),
            }, context_instance=RequestContext(request))
    raise Http404


@login_required
def view(request, message_id, *args, **kwargs):
    """Display one specific message."""
    return _view(request, Q(pk=message_id), *args, **kwargs)


@login_required
def view_conversation(request, thread_id, *args, **kwargs):
    """Display a conversation."""
    return _view(request, Q(thread=thread_id), *args, **kwargs)


def _update(request, field_bit, success_msg, field_value=None, success_url=None):
    """
    Code common to the archive/delete/undelete actions.

    Arguments:
        ``field_bit``: a part of the name of the field to update
        ``success_msg``: the displayed text in case of success
    Optional arguments:
        ``field_value``: the value to set in the field
        ``success_url``: where to redirect to after a successful POST

    """
    if not request.method == 'POST':
        raise Http404
    next_url = _get_referer(request) or 'postman_inbox'
    pks = request.POST.getlist('pks')
    tpks = request.POST.getlist('tpks')
    if pks or tpks:
        user = request.user
        filter = Q(pk__in=pks) | Q(thread__in=tpks)
        recipient_rows = Message.objects.as_recipient(user, filter).update(**{'recipient_{0}'.format(field_bit): field_value})
        sender_rows = Message.objects.as_sender(user, filter).update(**{'sender_{0}'.format(field_bit): field_value})
        if not (recipient_rows or sender_rows):
            raise Http404  # abnormal enough, like forged ids
        messages.success(request, success_msg, fail_silently=True)
        return redirect(request.GET.get('next', success_url or next_url))
    else:
        messages.warning(request, _("Select at least one object."), fail_silently=True)
        return redirect(next_url)


@login_required
def archive(request, *args, **kwargs):
    """Mark messages/conversations as archived."""
    return _update(request, 'archived', _("Messages or conversations successfully archived."), True, *args, **kwargs)


@login_required
def delete(request, *args, **kwargs):
    """Mark messages/conversations as deleted."""
    return _update(request, 'deleted_at', _("Messages or conversations successfully deleted."), now(), *args, **kwargs)


@login_required
def undelete(request, *args, **kwargs):
    """Revert messages/conversations from marked as deleted."""
    return _update(request, 'deleted_at', _("Messages or conversations successfully recovered."), *args, **kwargs)
