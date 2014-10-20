#!/usr/bin/env python
import echoprint
import subprocess
import sys
import struct
import slumber

import json

API_ENDPOINT = 'http://local.openbroadcast.org:8080/de/api/v1/'
API_AUTH = ("root", "root")


if len(sys.argv) < 2:
    print "Usage: identify.py filename"
    sys.exit(1)

filename = sys.argv[1]

try:
   with open(filename) as f: pass
except IOError as e:
    print "Unable to open file"
    sys.exit(1)




"""
#python module 
p = subprocess.Popen([
    'ffmpeg',
    '-i', filename,
    '-ac', '1',
    '-ar', '11025',
    '-f', 's16le',
    '-t', '30',
    '-ss', '10',
    '-',
], stdout=subprocess.PIPE)

samples = []

while True:
    sample = p.stdout.read(2)
    if sample == '':
        break
    samples.append(struct.unpack('h', sample)[0] / 32768.0)

d = echoprint.codegen(samples)

code = d['code']

"""

# binary

ecb = 'echoprint-codegen'

path = filename

#path = self.master_path

print 'path: %s' % path

p = subprocess.Popen([
    ecb, path, '12', '10',
], stdout=subprocess.PIPE)
stdout = p.communicate()        
d = json.loads(stdout[0])

code = d[0]['code']







api = slumber.API(API_ENDPOINT, auth=API_AUTH)

tracks = api.track.get(code=code, format='json')



if len(tracks['objects']) < 1:
    print '\nsorry - no match\n'
for track in tracks['objects']:
    print '---------------------------------------------------'
    print track['uuid']
    print track['resource_uri']
    print track['absolute_url']
    print
    #print track
    
print
print



#d['api_key'] = api_key
#res = requests.get('http://developer.echonest.com/api/v4/song/identify', d)

#print res

# r = requests.get('https://api.github.com', auth=('user', 'pass'))



#print res.content

