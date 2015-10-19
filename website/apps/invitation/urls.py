from django.conf.urls import *
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from app_settings import INVITE_ONLY




TemplateView.as_view(template_name='invitation/invitation_home.html')

urlpatterns = patterns('',
    url(r'^invitation/$',
        TemplateView.as_view(template_name='invitation/invitation_home.html'),
        name='invitation_home'),
    url(r'^invitation/invite/$',
        'invitation.views.invite',
        name='invitation_invite'),
    url(r'^invitation/invite/complete/$',
        TemplateView.as_view(template_name='invitation/invitation_complete.html'),
        name='invitation_complete'),
    url(r'^invitation/invite/unavailable/$',
        TemplateView.as_view(template_name='invitation/invitation_unavailable.html'),
        name='invitation_unavailable'),
    url(r'^invitation/accept/complete/$',
        TemplateView.as_view(template_name='invitation/invitation_registered.html'),
        name='invitation_registered'),
    url(r'^invitation/accept/(?P<invitation_key>\w+)/$',
        'invitation.views.register',
        name='invitation_register'),
)

