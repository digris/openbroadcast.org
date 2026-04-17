import pytest


from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase
from .. import views


# continue here...
# https://stackoverflow.com/questions/8603035/how-tdd-can-be-applied-to-django-class-based-generic-views


class TestAccountViews(TestCase):

    # pytestmark = pytest.mark.django_db
    def test_anonymous(self):

        req = RequestFactory().get("account/login/")

        middleware = SessionMiddleware()
        middleware.process_request(req)
        req.session.save()

        resp = views.UserLoginView.as_view()(req)
        assert resp.status_code == 200, "Should be callable by anyone"
