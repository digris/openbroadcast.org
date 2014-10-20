from django.conf.urls import patterns, url

from django_auth_policy.forms import (StrictAuthenticationForm,
                                      StrictPasswordChangeForm)


urlpatterns = patterns('',
    url(r'^login/$', 'django_auth_policy.views.login', name='login',
        kwargs={'authentication_form': StrictAuthenticationForm,
                'template_name': 'login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login',
        name='logout'),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change',
        name='password_change',
        kwargs={'password_change_form': StrictPasswordChangeForm,
                'template_name': 'change_password.html',
                'post_change_redirect': '/',
                }),
    )
