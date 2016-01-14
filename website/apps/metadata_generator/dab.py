# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib
import logging
import os
import time
from django.conf import settings
from django.template import loader
from wand.color import Color
from wand.image import Image
from wand.drawing import Drawing
from wand.compat import nested
from math import cos, pi, sin
from wand.image import Image, COMPOSITE_OPERATORS

log = logging.getLogger(__name__)

MEDIA_ROOT  = getattr(settings, 'MEDIA_ROOT')
MEDIA_URL  = getattr(settings, 'MEDIA_URL')

SLIDE_BASE_IMAGE = getattr(settings, 'DAB_SLIDE_BASE_IMAGE', os.path.join(
        os.path.dirname(__file__), 'asset', 'slide_base.png')
    )


SLIDE_BASE_FONT = getattr(settings, 'DAB_SLIDE_BASE_IMAGE', os.path.join(
        os.path.dirname(__file__), 'asset', 'HelveticaNeueCyr-Light.otf')
    )

SLIDE_DEFAULT_IMAGE = getattr(settings, 'DAB_SLIDE_DEFAULT_IMAGE', os.path.join(
        os.path.dirname(__file__), 'asset', 'default.png')
    )

SLIDE_BASE_DIR = os.path.join(MEDIA_ROOT, 'metadata', 'dab')
SLIDE_BASE_URL = MEDIA_URL + 'metadata/' +  'dab/'



class DABMetadataGenerator(object):

    def __init__(self, emission, content_object):

        self.emission = emission
        self.content_object = content_object

        log.debug('generate dab metadata for emission: %s - content_object: %s' % (self.emission, self.content_object))

        if not os.path.isdir(SLIDE_BASE_DIR):
            os.makedirs(SLIDE_BASE_DIR)


    def get_text(self):

        items = []

        if not (self.emission and self.content_object):
            return ['zzZzzZZZzzZZ']


        playlist = self.emission.content_object

        text = ''
        if playlist.series:
            text += '%s ' % playlist.series.name
            if playlist.series_number:
                text += '#%s ' % playlist.series_number
            text += ' - '

        text += '%s\n' % playlist.name

        if self.content_object.name:
            text += '%s by %s - %s\n' % (self.content_object.name, self.content_object.artist.name, self.content_object.release.name)

        if playlist.user:
            text += 'curated by %s' % playlist.user.profile.get_display_name()

        items.append(
            text
        )

        return items



    def get_slides(self):

        if not (self.emission and self.content_object):
            return [self.generate_slide(
                    primary_text='-',
                    secondary_text='-',
            )]

        items = []

        main_image_path = SLIDE_DEFAULT_IMAGE
        if self.content_object.release and self.content_object.release.main_image:
            main_image_path = self.content_object.release.main_image.path


        t = loader.get_template('metadata_generator/dab/slide_primary_text.txt')
        primary_text = t.render({
            'media': self.content_object
        })

        t = loader.get_template('metadata_generator/dab/slide_secondary_text.txt')
        secondary_text = t.render({
            'emission': self.emission,
            'playlist': self.emission.content_object
        })

        slide = self.generate_slide(
                    primary_text=primary_text,
                    secondary_text=secondary_text,
                    overlay_image_path=main_image_path
        )

        items.append(
            slide
        )

        return items

    def generate_slide(self, primary_text=None, secondary_text=None, overlay_image_path=None):

        self.clean_slides()


        if overlay_image_path:
            key = '%s-%s' % (self.emission.uuid, self.content_object.uuid)
            path = os.path.join(SLIDE_BASE_DIR, key + '.png')
            url = SLIDE_BASE_URL + key + '.png'
        else:
            overlay_image_path = SLIDE_DEFAULT_IMAGE
            key = 'default'
            path = os.path.join(SLIDE_BASE_DIR, key + '.png')
            url = SLIDE_BASE_URL + key + '.png'

        # if os.path.isfile(path):
        #     return url

        overlay_image = Image(filename=overlay_image_path)

        with Drawing() as draw:

            # add overlay image
            draw.composite('over', left=210, top=10, width=100, height=100, image=overlay_image)

            # text settings
            draw.font = SLIDE_BASE_FONT
            draw.font_size = 14
            draw.text_interline_spacing = 8
            draw.fill_color = Color('white')
            draw.text_antialias = True

            # draw text
            if primary_text:
                draw.text(10, 28, primary_text)

            if secondary_text:
                draw.font_size = 13
                draw.text_interline_spacing = 5
                draw.text(10, 140, secondary_text)


            # offset = 28
            # for line in primary_text:
            #     if len(line) > 28:
            #         line = '%s...' % line[0:25]
            #     draw.text(10, offset, line)
            #     offset += 24



            # draw.text(10, 20, self.content_object.name)
            # draw.text(10, 42, 'by %s' % self.content_object.artist.name)
            # draw.text(10, 64, '%s' % self.content_object.release.name)


            # compose image
            with Image(filename=SLIDE_BASE_IMAGE) as image:
                draw(image)
                image.save(filename=path)
                image.save(filename=os.path.join(SLIDE_BASE_DIR, 'debug.png'))




        return url


    def clean_slides(self, max_age=3600):

        # uuid-uuid.png -> 77 chars
        filename_length = 77

        for file in os.listdir(SLIDE_BASE_DIR):
            if file.endswith(".png"):
                path = os.path.join(SLIDE_BASE_DIR, file)
                fstat = os.stat(path)
                if len(file) == filename_length and fstat.st_mtime < time.time() - max_age:
                    log.info('file age: %s -> delete: %s' % (fstat.st_mtime, file))
                    os.unlink(path)






