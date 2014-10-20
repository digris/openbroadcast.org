#-*- coding: utf-8 -*-
import logging

try:
    from PIL import Image as PILImage
except ImportError:
    try:
        import Image as PILImage
    except ImportError:
        raise ImportError("The Python Imaging Library was not found.")
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from filer import settings as filer_settings
from filer.models.filemodels import File
from filer.utils.filer_easy_thumbnails import FilerThumbnailer
from filer.utils.pil_exif import get_exif_for_file
import os

logger = logging.getLogger("filer")

class Audio(File):
    SIDEBAR_IMAGE_WIDTH = 210
    DEFAULT_THUMBNAILS = {
        'admin_clipboard_icon': {'size': (32, 32), 'crop': True,
                                 'upscale': True},
        'admin_sidebar_preview': {'size': (SIDEBAR_IMAGE_WIDTH, 10000)},
        'admin_directory_listing_icon': {'size': (48, 48),
                                         'crop': True, 'upscale': True},
        'admin_tiny_icon': {'size': (32, 32), 'crop': True, 'upscale': True},
    }
    file_type = 'Audio'
    _icon = "Audio"

    
    bits_per_sample = models.PositiveIntegerField(default=0)
    sample_rate = models.PositiveIntegerField(default=0)
    total_frames = models.PositiveIntegerField(default=0)
    seconds_length = models.PositiveIntegerField(default=0)
    
    filetype = models.CharField(max_length=12,null=True, blank=True, help_text="File Type", editable=False)


    @classmethod
    def matches_file_type(cls, iname, ifile, request):
      iext = os.path.splitext(iname)[1].lower()
      print 'IEXT: %s' % iext
      return iext in ['.mp3', '.wav', '.ogg', '.mp4', '.aiff']

    def save(self, *args, **kwargs):
        self.has_all_mandatory_data = self._check_validity()        
        super(Audio, self).save(*args, **kwargs)

    def _check_validity(self):
        if not self.name:
            return False
        return True

    def sidebar_image_ratio(self):
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

    def has_generic_permission(self, request, permission_type):
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
            return self.folder.has_generic_permission(request, permission_type)
        else:
            return False

    @property
    def label(self):
        if self.name in ['', None]:
            return self.original_filename or 'unnamed file'
        else:
            return self.name

    @property
    def width(self):
        return self._width or 0

    @property
    def height(self):
        return self._height or 0

    @property
    def icons(self):
        _icons = {}
        for size in filer_settings.FILER_ADMIN_ICON_SIZES:
            try:
                thumbnail_options = {
                    'size': (int(size), int(size)),
                    'crop': True,
                    'upscale': True,
                    'subject_location': self.subject_location}
                thumb = self.file.get_thumbnail(thumbnail_options)
                _icons[size] = thumb.url
            except Exception, e:
                # catch exception and manage it. We can re-raise it for debugging
                # purposes and/or just logging it, provided user configured
                # proper logging configuration
                if filer_settings.FILER_ENABLE_LOGGING:
                    logger.error('Error while generating icons: %s',e)
                if filer_settings.FILER_DEBUG:
                    raise e
        return _icons

    @property
    def thumbnails(self):
        _thumbnails = {}
        for name, opts in Audio.DEFAULT_THUMBNAILS.items():
            try:
                opts.update({'subject_location': self.subject_location})
                thumb = self.file.get_thumbnail(opts)
                _thumbnails[name] = thumb.url
            except Exception,e:
                # catch exception and manage it. We can re-raise it for debugging
                # purposes and/or just logging it, provided user configured
                # proper logging configuration
                if filer_settings.FILER_ENABLE_LOGGING:
                    logger.error('Error while generating thumbnail: %s',e)
                if filer_settings.FILER_DEBUG:
                    raise e
        return _thumbnails

    @property
    def easy_thumbnails_thumbnailer(self):
        tn = FilerThumbnailer(file=self.file.file, name=self.file.name,
                         source_storage=self.file.source_storage,
                         thumbnail_storage=self.file.thumbnail_storage)
        return tn

    class Meta:
        app_label = 'filer'
        verbose_name = _('Audio')
        verbose_name_plural = _('Audios')








def audio_post_save(sender, **kwargs):
    
    obj = kwargs['instance']
    print "audiomodel post save"
    
    """
    if obj.is_public and obj.folder:
        print "still public... - with folder"
        obj.is_public = False
        obj.save()
    """
    if obj.is_public:
        pass
        #obj.is_public = False
        #obj.save()


    
    
 
post_save.connect(audio_post_save, sender=Audio)    




