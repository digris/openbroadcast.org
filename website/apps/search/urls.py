from django.conf.urls import url
from search import views

urlpatterns = [
    url(r'^$', views.index, name='search-index'),
]
