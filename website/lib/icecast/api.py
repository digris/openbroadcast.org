import requests
# logging
import logging
log = logging.getLogger(__name__)

class IcecastAPI:
    
    def __init__(self):
        pass
    
    def set_metadata(self, channel, text):

        log.info('setting metadata: %s' % text)
        
        print '*************************'
        # getting streaming setup
        server = channel.stream_server
        
        print server
        print 'server name: %s' % server.name
        print 'host:        %s' % server.host
        print 'admin:       %s' % server.admin_pass
        print 'mount:       %s' % server.mountpoint

        if server.meta_prefix:
            text = '%s %s' % (server.meta_prefix, text)

        try:
            self.update_server(server, '/%s' % server.mountpoint, text)
        except Exception, e:
            print e


    def update_server(self, server, mount, text):

        """
        url format:
        http://pypo:8000/admin/metadata?mount=/po_256&mode=updinfo&song=ACDC+Back+In+Black!!
        """
        log.debug('server: %s' % server)
        log.debug('mount: %s' % mount)
        
        url = '%sadmin/metadata' % server.host
        print '*******************'
        
        auth=('admin', server.admin_pass)
        
        params = {'mount': mount, 'mode': 'updinfo', 'song': u'%s' % text}
        
        r = requests.get(url, auth=auth, params=params, timeout=2.0)
        
        print '######################################################'
        print r.url
        print r.text
        print
        print

        