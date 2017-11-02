# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

import base64
import struct
import hashlib
from binascii import unhexlify

from django.conf import settings
from PIL import Image

from django.core.cache import cache

try:
    from StringIO import BytesIO
except ImportError:
    from io import BytesIO


DEFAULT_SIZE = [1, 1]
DEFAULT_COLOR = getattr(settings, 'PLACEHOLDER_IMAGE_DEFAULT_COLOR', '#ffffff')


def generate_image_placeholder(size, color):

    if not size:
        size = DEFAULT_SIZE

    if not color:
        color = DEFAULT_COLOR

    cache_key = 'image_placeholder{}'.format(hashlib.md5('{}{}'.format('x'.join(str(size)), color).encode('utf-8')).hexdigest())

    img_base64 = cache.get(cache_key)

    if img_base64:
        return u'data:image/png;base64,{}'.format(img_base64.decode("utf-8"))

    bg = struct.unpack('BBB', unhexlify(color.replace('#', '')))

    img = Image.new("RGB", (size[0], size[1]), bg)
    buffer = BytesIO()
    img.save(buffer, format="PNG")

    img_base64 = base64.b64encode(buffer.getvalue())

    cache.set(cache_key, img_base64, 60*60*24)

    return u'data:image/png;base64,{}'.format(img_base64.decode("utf-8"))
