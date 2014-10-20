import re

def get_service_by_url(url, service):

    if url.find('facebook.com') != -1:
        service = 'facebook'

    if url.find('youtube.com') != -1:
        service = 'youtube'

    if url.find('discogs.com') != -1:
        if url.find('/master/') != -1:
            service = 'discogs_master'
        else:
            service = 'discogs'

    if url.find('wikipedia.org') != -1:
        service = 'wikipedia'

    if url.find('last.fm') != -1 or url.find('lastfm') != -1:
        service = 'lastfm'

    if url.find('musicbrainz.org') != -1:
        service = 'musicbrainz'

    if url.find('soundcloud.com') != -1:
        service = 'soundcloud'

    if url.find('bandcamp.com') != -1:
        service = 'bandcamp'

    if url.find('itunes.apple.com') != -1:
        service = 'itunes'

    if url.find('linkedin.com') != -1:
        service = 'linkedin'

    if url.find('twitter.com') != -1:
        service = 'twitter'

    if not service:
        service = 'generic'

    return service




def uuid_by_url(url):
    """
    extracts an uuid from an url. e.g.:
    'http://musicbrainz.org/release/b442ed9b-0abf-48e5-bb2b-58a7fad4cb79/whatever'
    returns:
    'b442ed9b-0abf-48e5-bb2b-58a7fad4cb79'
    """
    re_uuid = re.compile("[0-F]{8}-[0-F]{4}-[0-F]{4}-[0-F]{4}-[0-F]{12}", re.I).findall(url)
    try:
        return re_uuid[0]
    except:
        return None


def uuid_by_object(obj, service='musicbrainz'):

    try:
        relations = obj.relations.filter(service=service)
        if relations.count() > 0:
            return uuid_by_url(relations[0].url)

    except:
        pass
