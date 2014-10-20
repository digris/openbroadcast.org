# storage related helpers
import os
import string
import unicodedata
import urllib2
import logging
import ntpath

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from django.conf import settings
from django.core.files.storage import FileSystemStorage

log = logging.getLogger(__name__)


class NoUUIDException(Exception):
    pass

def get_dir_for_object(obj, prefix=None, app_dir=None, object_dir=None):

    if not obj.uuid:
        raise NoUUIDException("get_dir_for_object needs an object with uuid property! and this property needs a value!")

    if not object_dir:
        object_dir = obj.__class__.__name__.lower()

    if not app_dir:
        try:
            app_dir = obj._meta.app_label.lower()
        except:
            app_dir = None

    path = os.path.join(object_dir, obj.uuid.replace('-', '/')[5:])

    if app_dir:
        path = os.path.join(app_dir, path)

    if prefix:
        path = os.path.join(prefix, path)

    return path


def safe_filename(str):
    log.debug('make safe: %s' % str)
    str = unicodedata.normalize('NFKD', str)
    return ''.join(ch for ch in str if ch not in "/\\'")


def get_file_from_url(url):

    log.info('try to get file from url: %s' % url)
    file_obj = None

    try:
        try:
            response = urllib2.urlopen(url)
            temp_file = NamedTemporaryFile(delete=True)
            temp_file.write(response.read())
            temp_file.flush()

            file_obj = File(temp_file)
        except Exception, e:
            log.warning('%s' % e)

    except Exception, e:
        log.warning('%s' % e)
        pass

    return file_obj


def get_file_from_path(path, filename=None):

    log.info('try to get file from path: %s' % path)
    file_obj = None

    try:
        f = open(path, 'r')
        temp_file = NamedTemporaryFile(delete=True)
        temp_file.write(f.read())
        temp_file.flush()
        f.close()

        if not filename:
            filename = ntpath.basename(path)

        else:
            filename = safe_filename(filename)


        file_obj = File(temp_file, filename)


    except Exception, e:
        log.warning('%s' % e)
        pass

    return file_obj



class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name):
        """
        Returns a filename that's free on the target storage system, and
        available for new content to be written to.
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name