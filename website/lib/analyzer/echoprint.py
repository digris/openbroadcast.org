#!/usr/bin/env python
import subprocess
import json

import requests


try:
    from settings import ECHOPRINT_CODEGEN_BIN
except Exception, e:
    print e
    ECHOPRINT_CODEGEN_BIN = 'echoprint-codegen'
    pass

class Echoprint:
    
    def full_echoprint_from_path(self, path):
        
        print ECHOPRINT_CODEGEN_BIN
        
        p = subprocess.Popen([
            ECHOPRINT_CODEGEN_BIN, path,
        ], stdout=subprocess.PIPE)
        stdout = p.communicate()        
        d = json.loads(stdout[0])
        
        code = None
        version = None
        try:
            code = d[0]['code']
            version = d[0]['metadata']['version']
            duration = d[0]['metadata']['duration']
        except Exception, e:
            print e
            pass
        
        return code, version, duration, d
    
    def echoprint_from_path(self, path, offset=10, duration=25):
        
        print ECHOPRINT_CODEGEN_BIN
        
        p = subprocess.Popen([
            ECHOPRINT_CODEGEN_BIN, path, '%s' % offset, '%s' % (offset + duration)
        ], stdout=subprocess.PIPE)
        stdout = p.communicate()        
        d = json.loads(stdout[0])
        
        code = None
        version = None
        try:
            code = d[0]['code']
            version = d[0]['metadata']['version']
            duration = d[0]['metadata']['duration']
        except Exception, e:
            print e
            pass
        
        return code, version, duration, d
    
    def get_by_echoprintfp(self, code, version):

        print code

        res = requests.get("http://localhost:8000/query?fp_code=%s" % code)
        
        print res

        return json.loads(res.text)


"""
e = Echoprint()
code, version, duration, d = e.full_echoprint_from_path(sys.argv[1])

print duration


# post
print "## ADDING TO SERVER"
payload = {
           'fp_code': code,
           'codever': version,
           'length': duration,
           'track_id': 'XYZIIIDDD',
           'track': 'Da Darling',
           }
r = requests.post("http://localhost:8080/ingest", data=payload)
print r.text

# try to get it

print "## TRYING TO LOOKUP"
payload = {
           'fp_code': code,
           }
r = requests.get("http://localhost:8080/query?fp_code=%s" % code)
print r.text
"""



#res = a.get_by_enmfp(code, version)




