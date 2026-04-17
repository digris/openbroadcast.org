from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.utils.translation import ugettext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.admin.views.decorators import staff_member_required
from .models import InvitationError, Invitation, InvitationStats
from .forms import InvitationForm, RegistrationFormInvitation
from registration.signals import user_registered


@login_required
def invite(
    request,
    success_url=None,
    form_class=InvitationForm,
    template_name="invitation/invitation_form.html",
    extra_context=None,
):

    if not request.user.has_perm("invitation.add_invitation"):
        return HttpResponseForbidden("Unauthorized")

    if request.method == "POST":
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            try:
                invitation = Invitation.objects.invite(
                    request.user,
                    form.cleaned_data["email"],
                    form.cleaned_data["message"],
                )
            except InvitationError as e:
                return HttpResponseRedirect(reverse("invitation:unavailable"))
            invitation.send_email(request=request)
            if "next" in request.GET:
                return HttpResponseRedirect(request.GET["next"])
            return HttpResponseRedirect(success_url or reverse("invitation:complete"))
    else:
        form = form_class()
    context = {"form": form}
    if extra_context:
        for key, value in extra_context.items():
            context[key] = value() if callable(value) else value
    return render(request, template_name, context)


def register(
    request,
    invitation_key,
    wrong_key_template="invitation/wrong_invitation_key.html",
    redirect_to_if_authenticated="/",
    success_url=None,
    form_class=RegistrationFormInvitation,
    template_name="registration/registration_form.html",
    extra_context=None,
):

    if request.user.is_authenticated():
        return HttpResponseRedirect(redirect_to_if_authenticated)
    try:
        invitation = Invitation.objects.find(invitation_key)
    except Invitation.DoesNotExist:
        context = {"invitation_key": invitation_key}
        if extra_context:
            for key, value in extra_context.items():
                context[key] = value() if callable(value) else value
        return render(request, wrong_key_template, context)
    if request.method == "POST":
        form = form_class(invitation.email, request.POST, request.FILES)
        if form.is_valid():
            new_user = form.save()
            invitation.mark_accepted(new_user)
            user_registered.send(sender="invitation", user=new_user, request=request)

            """
            bit hackish... authenticate & login the user
            """
            new_user.backend = "django.contrib.auth.backends.ModelBackend"
            login(request, new_user)
            return HttpResponseRedirect(new_user.get_absolute_url())
            # return HttpResponseRedirect(success_url or reverse('auth_login'))
    else:
        form = form_class(invitation.email)
    context = {"form": form}
    if extra_context:
        for key, value in extra_context.items():
            context[key] = value() if callable(value) else value
    return render(request, template_name, context)


@staff_member_required
def reward(request):
    """
    Add invitations to users with high invitation performance and redirect
    refferring page.
    """
    rewarded_users, invitations_given = InvitationStats.objects.reward()
    if rewarded_users:
        message = ugettext(
            "%(users)s users are given a total of " "%(invitations)s invitations."
        ) % {"users": rewarded_users, "invitations": invitations_given}
    else:
        message = ugettext(
            "No user has performance above " "threshold, no invitations awarded."
        )
    request.user.message_set.create(message=message)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
