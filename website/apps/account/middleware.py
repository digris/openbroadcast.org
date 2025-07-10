import six
from django.contrib import messages

from social_django.middleware import (
    SocialAuthExceptionMiddleware as BaseSocialAuthExceptionMiddleware,
)


class SocialAuthExceptionMiddleware(BaseSocialAuthExceptionMiddleware):
    def raise_exception(self, request, exception):
        # return False to test 'real' behaviour
        print(exception)
        return False

    def get_redirect_uri(self, request, exception):
        redirect_to = request.GET.get("next")
        if redirect_to:
            return redirect_to
        return super().get_redirect_uri(
            request, exception
        )

    def get_message(self, request, exception):
        message = str(exception)
        if message == "":
            message = f"{exception.__class__}"

        return message
