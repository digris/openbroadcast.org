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

DEFAULT_DLS_TEXT = 'Open Broadcast'

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
        self.playlist = emission.content_object if emission else None
        self.content_object = content_object

        log.debug('generate dab metadata for emission: %s - content_object: %s' % (self.emission, self.content_object))

        if not os.path.isdir(SLIDE_BASE_DIR):
            os.makedirs(SLIDE_BASE_DIR)


    def get_text(self):

        items = []

        if not (self.emission and self.content_object):
            return [DEFAULT_DLS_TEXT]


        playlist = self.playlist

        text = ''
        if self.playlist.series:
            text += '%s ' % self.playlist.series.name
            if self.playlist.series_number:
                text += '#%s ' % self.playlist.series_number
            text += ' - '

        text += '%s\n' % self.playlist.name

        if self.content_object.name:
            text += '%s by %s - %s\n' % (self.content_object.name, self.content_object.artist.name, self.content_object.release.name)

        if self.playlist.user:
            text += 'curated by %s' % self.playlist.user.profile.get_display_name()

        items.append(
            text
        )

        return items



    def get_slides(self):

        if not (self.emission and self.content_object):
            return [self.compose_main_slide(
                    primary_text='-',
                    secondary_text='-',
            )]


        self.clean_slides()

        items = []
        slide_id = 0

        ######################################################################
        # main slide, including image & text                                 #
        ######################################################################

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

        slide = self.compose_main_slide(
            primary_text=primary_text,
            secondary_text=secondary_text,
            overlay_image_path=main_image_path,
            slide_id=slide_id
        )

        items.append(
            slide
        )
        slide_id +=1

        ######################################################################
        # additional slides                                                  #
        ######################################################################
        if self.content_object.artist and self.content_object.artist.main_image and os.path.isfile(self.content_object.artist.main_image.path):

            slide = self.compose_image_slide(
                image_path=self.content_object.artist.main_image.path,
                slide_id=slide_id
            )

            items.append(
                slide
            )
            slide_id +=1

        if self.playlist.main_image and os.path.isfile(self.playlist.main_image.path):

            slide = self.compose_image_slide(
                image_path=self.playlist.main_image.path,
                slide_id=slide_id
            )

            items.append(
                slide
            )
            slide_id +=1


        return items


    def compose_main_slide(self, primary_text=None, secondary_text=None, overlay_image_path=None, slide_id=0):

        if overlay_image_path and os.path.isfile(overlay_image_path):
            key = '%s-%s-%03d' % (self.emission.uuid, self.content_object.uuid, slide_id)
            path = os.path.join(SLIDE_BASE_DIR, key + '.png')
            url = SLIDE_BASE_URL + key + '.png'
        else:
            overlay_image_path = SLIDE_DEFAULT_IMAGE
            key = 'default'
            path = os.path.join(SLIDE_BASE_DIR, key + '.png')
            url = SLIDE_BASE_URL + key + '.png'

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

            # compose image
            with Image(filename=SLIDE_BASE_IMAGE) as image:
                draw(image)
                image.save(filename=path)
                image.save(filename=os.path.join(SLIDE_BASE_DIR, 'debug-%s.png' % slide_id))

        return url


    def compose_image_slide(self, image_path=None, text=None, slide_id=1):

        image_display_size = (300, 190)

        key = '%s-%s-%03d' % (self.emission.uuid, self.content_object.uuid, slide_id)
        path = os.path.join(SLIDE_BASE_DIR, key + '.png')
        url = SLIDE_BASE_URL + key + '.png'

        overlay_image = Image(filename=image_path)

        with Drawing() as draw:

            # add overlay image

            size = overlay_image.size

            if size[0] > size[1]:
                orientation = 'landscape'
                scale = float(image_display_size[1]) / float(size[1])
            else:
                orientation = 'portrait'
                scale = float(image_display_size[1]) / float(size[0])


            print scale
            print orientation

            overlay_image.resize(int(size[0] * scale), int(size[1] * scale))

            size = overlay_image.size
            print size

            #if orientation == 'portrait':
            width = 190
            height = 190
            overlay_image.crop(10, 0, width=width, height=height)


            draw.composite('over', left=int(width/2) - 20, top=10, width=width, height=height, image=overlay_image)

            # text settings
            draw.font = SLIDE_BASE_FONT
            draw.font_size = 14
            draw.text_interline_spacing = 8
            draw.fill_color = Color('white')
            draw.text_antialias = True

            # draw text
            if text:
                draw.text(220, 10, text)


            # compose image
            with Image(filename=SLIDE_BASE_IMAGE) as image:
                draw(image)
                image.save(filename=path)
                image.save(filename=os.path.join(SLIDE_BASE_DIR, 'debug-%s.png' % slide_id))




        return url


    def clean_slides(self, max_age=3600):

        # uuid-uuid-000.png -> 81 chars
        filename_length = 81

        for file in os.listdir(SLIDE_BASE_DIR):
            if file.endswith(".png"):
                path = os.path.join(SLIDE_BASE_DIR, file)
                fstat = os.stat(path)
                if len(file) == filename_length and fstat.st_mtime < time.time() - max_age:
                    log.info('file age: %s -> delete: %s' % (fstat.st_mtime, file))
                    os.unlink(path)





