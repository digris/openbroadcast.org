import os.path

from django.conf import settings


def _convert_file_to_url(filename):
    relpath = os.path.relpath(filename, settings.SENDFILE_ROOT)

    # relpath = filename

    print 'filename: %s' % filename
    print 'sf root:  %s' % settings.SENDFILE_ROOT
    print 'sf url:   %s' % settings.SENDFILE_URL

    t = filename.split(settings.SENDFILE_ROOT)
    print t

    
    url = [settings.SENDFILE_URL]

    #print 'relpath: %s' % relpath
    #print 'url:       %s' % url

    while relpath:
        relpath, head = os.path.split(relpath)

        #print 'rp:   %s' % relpath
        #print 'head: %s' % head

        url.insert(1, head)

    print 'final: %s' % u'/'.join(url)

    #return u'/media/private/27ce367d/a841/11e2/996d/b8f6b11a3aed/cache/waveform.png'

    return u'/'.join(url)

