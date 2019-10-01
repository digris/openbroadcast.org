from django.conf.urls import *

urlpatterns = patterns(
    "", url(r"^simple/action/$", "simpleAction", name="simpleAction")
)
