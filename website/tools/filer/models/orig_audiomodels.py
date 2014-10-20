#-*- coding: utf-8 -*-
import os

from PIL import Image as PILImage
from django.db import models
from django.utils.translation import ugettext_lazy as _

from filer.models.filemodels import File
from filer.utils.filer_easy_thumbnails import FilerThumbnailer
from filer.utils.pil_exif import get_exif_for_file


# cross imports
# from alibrary.models import Artist, License

class Audio(File):
    SIDEBAR_Audio_WIDTH = 210
    DEFAULT_THUMBNAILS = {
        'admin_clipboard_icon': {'size': (32, 32), 'crop': True,
                                 'upscale': True},
        'admin_sidebar_preview': {'size': (SIDEBAR_Audio_WIDTH, 10000)},
        'admin_directory_listing_icon': {'size': (48, 48),
                                         'crop': True, 'upscale': True},
        'admin_tiny_icon': {'size': (32, 32), 'crop': True, 'upscale': True},
    }
    file_type = 'Audio'
    
    bits_per_sample = models.PositiveIntegerField(default=0)
    sample_rate = models.PositiveIntegerField(default=0)
    total_frames = models.PositiveIntegerField(default=0)
    seconds_length = models.PositiveIntegerField(default=0)
    
    filetype = models.CharField(max_length=12,null=True, blank=True, help_text="File Type", editable=False)
    

    # additional metadata
    # tracknumber = models.PositiveIntegerField(max_length=3, default=0)
    
    # relations
    # artist = models.ForeignKey(Artist, blank=True, null=True, related_name='audio_artist')
    # license = models.ForeignKey(License, blank=True, null=True, related_name='audio_license')
    
    _icon = "Audio"

    @classmethod
    def matches_file_type(cls, iname, ifile, request):
      # This was originally in admin/clipboardadmin.py  it was inside of a try
      # except, I have moved it here outside of a try except because I can't
      # figure out just what kind of exception this could generate... all it was
      # doing for me was obscuring errors...
      # --Dave Butler <croepha@gmail.com>
      iext = os.path.splitext(iname)[1].lower()
      
      print 'IEXT:'
      print iext
      
      return iext in ['.mp3','.flac','.m4a','.mp4','.wav','.aiff','.ogg']

    def save(self, *args, **kwargs):
        
        # audio-files _never_ should be public
        self.is_public = False;

        self.has_all_mandatory_data = self._check_validity()
        try:
            # do this more efficient somehow?
            self.file.seek(0)
            self._width, self._height = PILImage.open(self.file).size
        except Exception:
            # probably the Audio is missing. nevermind.
            pass
        super(Audio, self).save(*args, **kwargs)

    def _check_validity(self):
        if not self.name:
            return False
        return True

    def sidebar_Audio_ratio(self):
        if self.width:
            return float(self.width) / float(self.SIDEBAR_Audio_WIDTH)
        else:
            return 1.0

    def _get_exif(self):
        if hasattr(self, '_exif_cache'):
            return self._exif_cache
        else:
            if self.file:
                self._exif_cache = get_exif_for_file(self.file.path)
            else:
                self._exif_cache = {}
        return self._exif_cache
    exif = property(_get_exif)

    def has_edit_permission(self, request):
        return self.has_generic_permission(request, 'edit')

    def has_read_permission(self, request):
        return self.has_generic_permission(request, 'read')

    def has_add_children_permission(self, request):
        return self.has_generic_permission(request, 'add_children')

    def has_generic_permission(self, request, type):
        """
        Return true if the current user has permission on this
        Audio. Return the string 'ALL' if the user has all rights.
        """
        user = request.user
        if not user.is_authenticated() or not user.is_staff:
            return False
        elif user.is_superuser:
            return True
        elif user == self.owner:
            return True
        elif self.folder:
            return self.folder.has_generic_permission(request, type)
        else:
            return False

    @property
    def label(self):
        if self.name in ['', None]:
            return self.original_filename or 'unnamed file'
        else:
            return self.name


    class Meta:
        app_label = 'filer'
        verbose_name = _('Track')
        verbose_name_plural = _('Tracks')
