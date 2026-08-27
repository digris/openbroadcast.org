from django.conf.urls import url
from . import views

app_name = "player"
urlpatterns = [
    url(r"^$", views.PlayerIndexView.as_view(), name="player-index"),
    url(r"^next/$", views.PlayerNextIndexView.as_view(), name="player-index")
]

