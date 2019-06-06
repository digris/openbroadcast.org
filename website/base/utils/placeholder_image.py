# -*- coding: utf-8 -*-

import base64
import hashlib

from PIL import Image
from django.core.cache import cache

try:
    from StringIO import BytesIO
except ImportError:
    from io import BytesIO

DEFAULT_SIZE = [1, 1]


def generate_placeholder_image(size=None):

    if not size:
        size = DEFAULT_SIZE

    cache_key = "image_placeholder_{}".format(
        hashlib.md5("x".join(str(size)).encode("utf-8")).hexdigest()
    )

    img_base64 = cache.get(cache_key)

    if img_base64:
        return "data:image/png;base64,{}".format(img_base64)

    buffer = BytesIO()
    img = Image.new("RGBA", (size[0], size[1]), (255, 0, 0, 100))
    img.save(buffer, format="PNG")

    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    cache.set(cache_key, img_base64, 60 * 60 * 24)

    return "data:image/png;base64,{}".format(img_base64)
