# -*- coding: utf-8 -*-
import os
from django.conf import settings

BASE_DIR = getattr(settings, "BASE_DIR")

################################################################################
# api-related
################################################################################

# google related
GOOGLE_MAPS_API_KEY = "ABQIAAAAOHPJc2-0TzaYgfOquRJgtRR2_LvdznTgfqpGEUf18uq-dm_lmhSjdzKrt5n5UfFjwviK9F39LyXJng"

# facebook oauth settings
FACEBOOK_APP_ID = "108235479287674"
FACEBOOK_SECRET_KEY = "a5b0a3ce9f47d1eadaf004ffd9da4e1f"
FACEBOOK_API_SECRET = "a5b0a3ce9f47d1eadaf004ffd9da4e1f"
FACEBOOK_EXTENDED_PERMISSIONS = ["email", "publish_stream"]

# echonest analyzer
ECHONEST_API_KEY = "DC7YKF3VYN7R0LG1M"
