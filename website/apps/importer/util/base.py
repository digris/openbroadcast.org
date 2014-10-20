import logging
import time
import discogs_client as discogs
import requests
from django.conf import settings

DISCOGS_HOST = getattr(settings, 'DISCOGS_HOST', None)

log = logging.getLogger(__name__)




def discogs_image_by_url(url, type='uri'):

    image = None
    discogs.user_agent = "NRG Processor 0.01 http://anorg.net/"

    log.debug('search image for %s' % url)

    try:
        id = url.split('/')
        id = id[-1]
    except Exception, e:
        log.warning('inable to extract id: %s' % e)
        id = None

    if id:
        log.debug('Lookup image for discog id: %s' % (id))

        type = None
        if '/master/' in url:
            type = 'masters'

        if '/release/' in url:
            type = 'releases'

        if '/artist/' in url:
            type = 'artists'

        if '/label/' in url:
            type = 'labels'

        log.debug('Type is "%s"' % type)

        if type:

            url = 'http://%s/%s/%s' %(DISCOGS_HOST, type, id)
            log.debug('constructed API url "%s"' % url)

            r = requests.get(url)

            if not r.status_code == 200:
                log.warning('server error: %s %s' % (r.status_code, r.text))
                return

            try:
                response = r.json()

                if 'images' in response:
                    image = None
                    images = response['images']

                    for img in images:
                        if img['type'] == 'primary':
                            image = img['resource_url']

                    if not image:
                        for img in images:
                            if img['type'] == 'secondary':
                                image = img['resource_url']

                    if image:
                        return image

            except:
                pass

            pass




def discogs_id_by_url(url, type='uri'):
    
    log = logging.getLogger('importer.base.discogs_artist_id_by_url')
    
    discogs_id = None
    
    discogs.user_agent = "NRG Processor 0.01 http://anorg.net/"
    
    try:
        id = url.split('/')
        id = id[-1]
        
        if '/master/' in url:
            log.debug('Type is "master-release"')
            item = discogs.MasterRelease(int(id))
        
        if '/release/' in url:
            log.debug('Type is "release"')
            item = discogs.Release(int(id))
        
        if '/artist/' in url:
            log.debug('Type is "artist"')
            item = discogs.Artist(id)
                        
        time.sleep(1.1)

        
        discogs_id = item.data['id']



    except Exception, e:
        log.info('Unable to get id: %s', e)


    log.debug('Got id: %s' % (discogs_id))

    return discogs_id





def __old__discogs_image_by_url(url, type='uri'):

    log = logging.getLogger('importer.base.discogs_image_by_url')

    image = None

    discogs.user_agent = "NRG Processor 0.01 http://anorg.net/"

    try:
        id = url.split('/')
        id = id[-1]

        log.debug('Lookup image for discog id: %s' % (id))

        if '/master/' in url:
            log.debug('Type is "master-release"')
            item = discogs.MasterRelease(int(id))

        if '/release/' in url:
            log.debug('Type is "release"')
            item = discogs.Release(int(id))

        if '/artist/' in url:
            log.debug('Type is "artist"')
            item = discogs.Artist(id)

        time.sleep(1.1)

        imgs = item.data['images']
        have_img = False

        for img in imgs:
            if img['type'] == 'primary':
                print img
                image = img[type]
                have_img = True

        if not have_img:
            for img in imgs:
                if img['type'] == 'secondary':
                    print img
                    image = img[type]


    except Exception, e:
        log.info('Unable to get image: %s', e)


    log.debug('Got image at: %s' % (image))

    return image.replace('api.discogs.com', DISCOGS_HOST)