from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.translation import ugettext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.admin.views.decorators import staff_member_required
from models import InvitationError, Invitation, InvitationStats
from forms import InvitationForm, RegistrationFormInvitation
from registration.signals import user_registered


def apply_extra_context(context, extra_context=None):
    if extra_context is None:
        extra_context = {}
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return context


@login_required
def invite(request, success_url=None,
           form_class=InvitationForm,
           template_name='invitation/invitation_form.html',
           extra_context=None):

    if not request.user.has_perm('invitation.add_invitation'):
        return HttpResponseForbidden('Unauthorized')


    """
    Create an invitation and send invitation email.

    Send invitation email and then redirect to success URL if the
    invitation form is valid. Redirect named URL ``invitation_unavailable``
    on InvitationError. Render invitation form template otherwise.

    **Required arguments:**

    None.

    **Optional arguments:**

    :success_url:
        The URL to redirect to on successful registration. Default value is
        ``None``, ``invitation_complete`` will be resolved in this case.

    :form_class:
        A form class to use for invitation. Takes ``request.user`` as first
        argument to its constructor. Must have an ``email`` field. Custom
        validation can be implemented here.

    :template_name:
        A custom template to use. Default value is
        ``invitation/invitation_form.html``.

    :extra_context:
        A dictionary of variables to add to the template context. Any
        callable object in this dictionary will be called to produce
        the end result which appears in the context.

    **Template:**

    ``invitation/invitation_form.html`` or ``template_name`` keyword
    argument.

    **Context:**

    A ``RequestContext`` instance is used rendering the template. Context,
    in addition to ``extra_context``, contains:

    :form:
        The invitation form.
    """
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            try:
                invitation = Invitation.objects.invite(
                                     request.user, form.cleaned_data["email"], form.cleaned_data["message"])
            except InvitationError, e:
                print '****'
                print e
                print '****'
                return HttpResponseRedirect(reverse('invitation_unavailable'))
            invitation.send_email(request=request)
            if 'next' in request.REQUEST:
                return HttpResponseRedirect(request.REQUEST['next'])
            return HttpResponseRedirect(success_url or reverse('invitation_complete'))
    else:
        form = form_class()
    context = apply_extra_context(RequestContext(request), extra_context)
    return render_to_response(template_name,
                              {'form': form},
                              context_instance=context)


def register(request,
             invitation_key,
             wrong_key_template='invitation/wrong_invitation_key.html',
             redirect_to_if_authenticated='/',
             success_url=None,
             form_class=RegistrationFormInvitation,
             template_name='registration/registration_form.html',
             extra_context=None):
    """
    Allow a new user to register via invitation.

    Send invitation email and then redirect to success URL if the
    invitation form is valid. Redirect named URL ``invitation_unavailable``
    on InvitationError. Render invitation form template otherwise. Sends
    registration.signals.user_registered after creating the user.

    **Required arguments:**

    :invitation_key:
        An invitation key in the form of ``[\da-e]{40}``

    **Optional arguments:**

    :wrong_key_template:
        Template to be used when an invalid invitation key is supplied.
        Default value is ``invitation/wrong_invitation_key.html``.

    :redirect_to_if_authenticated:
        URL to be redirected when an authenticated user calls this view.
        Defaults value is ``/``

    :success_url:
        The URL to redirect to on successful registration. Default value is
        ``None``, ``invitation_registered`` will be resolved in this case.

    :form_class:
        A form class to use for registration. Takes the invited email as first
        argument to its constructor.

    :template_name:
        A custom template to use. Default value is
        ``registration/registration_form.html``.

    :extra_context:
        A dictionary of variables to add to the template context. Any
        callable object in this dictionary will be called to produce
        the end result which appears in the context.

    **Templates:**

    ``invitation/invitation_form.html`` or ``template_name`` keyword
    argument as the *main template*.

    ``invitation/wrong_invitation_key.html`` or ``wrong_key_template`` keyword
    argument as the *wrong key template*.

    **Context:**

    ``RequestContext`` instances are used rendering both templates. Context,
    in addition to ``extra_context``, contains:

    For wrong key template
        :invitation_key: supplied invitation key

    For main template
        :form:
            The registration form.
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(redirect_to_if_authenticated)
    try:
        invitation = Invitation.objects.find(invitation_key)
    except Invitation.DoesNotExist:
        context = apply_extra_context(RequestContext(request), extra_context)
        return render_to_response(wrong_key_template,
                                  {'invitation_key': invitation_key},
                                  context_instance=context)
    if request.method == 'POST':
        form = form_class(invitation.email, request.POST, request.FILES)
        if form.is_valid():
            new_user = form.save()
            invitation.mark_accepted(new_user)
            user_registered.send(sender="invitation",
                                 user=new_user,
                                 request=request)
            # return HttpResponseRedirect(success_url or reverse('invitation_registered'))
            # return HttpResponseRedirect(success_url or reverse('profiles-profile-detail', kwargs={'slug':new_user.username}))

            """
            bit hackish... authenticate & login the user
            """
            new_user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, new_user)
            return HttpResponseRedirect(new_user.get_absolute_url())
            #return HttpResponseRedirect(success_url or reverse('auth_login'))
    else:
        form = form_class(invitation.email)
    context = apply_extra_context(RequestContext(request), extra_context)
    return render_to_response(template_name,
                              {'form': form},
                              context_instance=context)


@staff_member_required
def reward(request):
    """
    Add invitations to users with high invitation performance and redirect
    refferring page.
    """
    rewarded_users, invitations_given = InvitationStats.objects.reward()
    if rewarded_users:
        message = ugettext(u'%(users)s users are given a total of ' \
                           u'%(invitations)s invitations.') % {
                                            'users': rewarded_users,
                                            'invitations': invitations_given}
    else:
        message = ugettext(u'No user has performance above ' \
                           u'threshold, no invitations awarded.')
    request.user.message_set.create(message=message)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
