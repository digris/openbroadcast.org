from django.conf.urls import url
from django.views.generic.base import TemplateView

from invitation import views

TemplateView.as_view(template_name="invitation/invitation_home.html")

app_name = "invitation"

urlpatterns = [
    url(
        r"^invitation/$",
        TemplateView.as_view(template_name="invitation/invitation_home.html"),
        name="home",
    ),
    url(r"^invitation/invite/$", views.invite, name="invitation_invite"),
    url(
        r"^invitation/invite/complete/$",
        TemplateView.as_view(template_name="invitation/invitation_complete.html"),
        name="complete",
    ),
    url(
        r"^invitation/invite/unavailable/$",
        TemplateView.as_view(template_name="invitation/invitation_unavailable.html"),
        name="unavailable",
    ),
    url(
        r"^invitation/accept/complete/$",
        TemplateView.as_view(template_name="invitation/invitation_registered.html"),
        name="registered",
    ),
    url(
        r"^invitation/accept/(?P<invitation_key>\w+)/$",
        views.register,
        name="register",
    ),
]
