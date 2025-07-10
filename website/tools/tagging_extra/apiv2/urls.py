from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^tag/$", views.tag_list, name="tag-list"),
]
