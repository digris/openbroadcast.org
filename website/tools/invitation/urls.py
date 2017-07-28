from django.conf.urls import url
from django.views.generic.base import TemplateView

from invitation import views

TemplateView.as_view(template_name='invitation/invitation_home.html')

urlpatterns = [
    url(r'^invitation/$',
        TemplateView.as_view(template_name='invitation/invitation_home.html'),
        name='invitation_home'),
    url(r'^invitation/invite/$',
        views.invite,
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
        views.register,
        name='invitation_register'),
]
