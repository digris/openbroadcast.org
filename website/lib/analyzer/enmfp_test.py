#!/usr/bin/env python
import subprocess
import sys
import json

import requests


if len(sys.argv) < 1:
    print "Usage: identify.py filename"
    sys.exit(1)


filename = sys.argv[1]


ECHONEST_API_KEY = 'DC7YKF3VYN7R0LG1M'

api_key = ECHONEST_API_KEY

"""
# raw audio data extraction
p = subprocess.Popen([
    'ffmpeg',
    '-i', filename,
    '-ac', '1',
    '-ar', '11025',
    '-f', 's16le',
    '-t', '30',
    '-ss', '0',
    '-',
], stdout=subprocess.PIPE)

samples = []

while True:
    sample = p.stdout.read(2)
    if sample == '':
        break
    samples.append(struct.unpack('h', sample)[0] / 32768.0)
"""

p = subprocess.Popen([
    'bin/codegen.Darwin', filename, '10', '40',
], stdout=subprocess.PIPE)

stdout = p.communicate()

d = json.loads(stdout[0])



code = d[0]['code']

payload = {}

payload['api_key'] = api_key
payload['version'] = '3.16'
#payload['query'] = '@json_string.json'
payload['code'] = code
payload['bucket'] = ('id:musicbrainz','id:spotify-WW', 'audio_summary')

print '******'
print payload
print '******'


res = requests.get('http://developer.echonest.com/api/v4/song/identify', params=payload)

print res.content

