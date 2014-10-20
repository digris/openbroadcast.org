from django.conf.urls.defaults import *


import views

urlpatterns = patterns("",
    url(r"^signup/$", views.signup, name="ajax_signup"),
    url(r"^login/$", views.login, name="ajax_signin"),
)
