from django import template
from django.apps import apps

Profile = apps.get_model("profiles", "profile")

register = template.Library()
