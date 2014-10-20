import itertools
import re

from django.utils import six
try:
    from PIL import Image, ImageChops, ImageFilter
except ImportError:
    import Image
    import ImageChops
    import ImageFilter

from PIL import ImageOps

from easy_thumbnails import utils

def colorize(im, colorize=None, **kwargs):

    if colorize:
        print 'colorize: %s' % colorize
        black = '#333333'
        white = '#ffffff'

        im = ImageOps.colorize(ImageOps.grayscale(im), black, white)


    return im