import os
from os.path import basename
from urlparse import urlsplit
import urllib2

from django.core.files import File as DjangoFile
from filer.models import Image

import logging
log = logging.getLogger(__name__)

def url2name(url):
    return basename(urlsplit(url)[2])

def download(url, dir):
    
    local_name = url2name(url)
    local_dir = dir
    local_path = '%s/%s' % (local_dir, local_name)

    
    req = urllib2.Request(url)
    r = urllib2.urlopen(req)
    
    if r.info().has_key('Content-Disposition'):
        # If the response has Content-Disposition, we take file name from it
        local_name = r.info()['Content-Disposition'].split('filename=')[1]
        if local_name[0] == '"' or local_name[0] == "'":
            local_name = local_name[1:-1]
    elif r.url != url: 
        # if we were redirected, the real file name we take from the final URL
        local_name = url2name(r.url)

    f = open(local_path, 'wb')
    f.write(r.read())
    f.close()
    
    return local_name, local_path
    
    
def url_to_file(url, folder):
    
    log.debug('saving %s to %s' % (url, folder))
    
    local_name, local_path = download(url, 'tmp')
    
    dj_file = DjangoFile(open(local_path), name=local_name)

    obj, created = Image.objects.get_or_create(
                                    original_filename=local_name,
                                    file=dj_file,
                                    folder=folder,
                                    is_public=True)

    os.remove(local_path)
    
    return obj


def path_to_file(path, folder):

    log.debug('saving %s to %s' % (path, folder))

    dj_file = DjangoFile(open(path), name=os.path.basename(path))

    obj, created = Image.objects.get_or_create(
                                    original_filename=os.path.basename(path),
                                    file=dj_file,
                                    folder=folder,
                                    is_public=True)



    return obj