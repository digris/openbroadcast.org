import requests
import logging
log = logging.getLogger(__name__)

class IcecastAPIClient:
    
    def __init__(self, channel):
        self.channel = channel
        if self.channel and self.channel.stream_server:
            self.server = self.channel.stream_server
        else:
            log.warning(u'unable to get streaming server for channel: %s' % self.channel)
            self.server = None


    def set_text(self, text):

        if self.server and self.server.meta_prefix:
            text = u'%s %s' % (self.server.meta_prefix, text)

        if self.server:

            url = '%sadmin/metadata' % self.server.host
            auth=(self.server.admin_user, self.server.admin_pass)
            params = {
                'mount': '/%s' % self.server.mountpoint,
                'mode': 'updinfo',
                'song': u'%s' % text
            }
            r = requests.get(url, auth=auth, params=params, timeout=2.0)

            if not r.status_code == 200:
                log.warning('API: %s - status: %s' % (r.url, r.status_code))
            else:
                log.debug('API: %s - status: %s' % (r.url, r.status_code))


def set_stream_metadata(channel, text):
    log.info(u'channel: %s - metadata-text: %s' % (channel, text))
    try:
        api = IcecastAPIClient(channel=channel)
        api.set_text(text)
    except Exception as e:
        log.warning(u'unable to set stream metadata text: %s' % e)
