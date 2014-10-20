# -*- coding: utf-8 -*-
from django.conf import settings

from social_auth.middleware import SocialAuthExceptionMiddleware

class SocialAuthExceptionExtraMiddleware(SocialAuthExceptionMiddleware):

    def get_redirect_uri(self, request, exception):
        
        if request.user:
            # TODO: should be edit url
            return request.user.get_absolute_url()
        
        return settings.LOGIN_ERROR_URL