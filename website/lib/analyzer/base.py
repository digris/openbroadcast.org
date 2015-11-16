#!/usr/bin/env python
import subprocess
import json
from django.conf import settings
import requests
ENMFP_CODEGEN_BINARY = getattr(settings, 'ENMFP_CODEGEN_BINARY', True)
ECHONEST_API_KEY = getattr(settings, 'ECHONEST_API_KEY', True)

class Analyze:
    
    def enmfp_from_path(self, path):
        
        print ENMFP_CODEGEN_BINARY
        
        p = subprocess.Popen([
            ENMFP_CODEGEN_BINARY, path, '10', '40',
        ], stdout=subprocess.PIPE)
        stdout = p.communicate()        
        d = json.loads(stdout[0])
        
        code = None
        version = None
        try:
            code = d[0]['code']
            version = d[0]['metadata']['version']
        except Exception, e:
            print e
            pass
        
        return code, version, d
    
    def get_by_enmfp(self, code, version):
        
        payload = {}        
        payload['api_key'] = ECHONEST_API_KEY
        payload['version'] = '3.16'
        payload['code'] = code
        #payload['bucket'] = ('id:musicbrainz','id:spotify-WW', 'audio_summary')
        payload['bucket'] = ('id:musicbrainz',)
        
        #print '******'
        #print payload
        #print '******'
        
        
        res = requests.get('http://developer.echonest.com/api/v4/song/identify', params=payload)
        
        print res.content
        
        return res.content



#a = Analyze()
#code, version = a.enmfp_from_path(sys.argv[1])
#res = a.get_by_enmfp(code, version)




