#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author Jonas Ohrstrom <jonas@digris.ch>

"""
Python part of radio playout (bcmon)

This function acts as a gateway between liquidsoap and the obp-api.
Mainliy used to tell the plattform what bcmon/LS does.

Main case: 
 - whenever LS starts playing a new track, its on_metadata callback calls
   a function in ls (notify(m)) which then calls the pythin script here
   with the currently starting filename as parameter 
 - this python script takes this parameter, tries to extract the actual
   media id from it, and then calls back to obp via api to tell about
   
   /Users/ohrstrom/srv/openbroadcast.org-upgrade/lib/python2.7/site-packages/django/./http/__init__.py
   remove: # 
   l 327


"""

# python defaults (debian default)
import time
import os
import traceback
from optparse import OptionParser
import sys
import subprocess
import time
import datetime
import logging
import logging.config
import urllib
import urllib2
import string
import telnetlib

import slumber

# additional modules (should be checked)
from configobj import ConfigObj

# custom imports
from util import *
from api import *
#from dls import *



BCMON_VERSION = '0.1'
API_MIN_VERSION = 20110201 # required obp version

API_ENDPOINT = 'http://openbroadcast.org.node05.daj.anorg.net/api/v1/'
API_AUTH = ("bcmon", "bcmon")

REC_OFFSET = 10
REC_DURATION = 50

CHANNELS_FILE = 'include_stations.liq'


#set up command-line options
parser = OptionParser()

# help screeen / info
usage = "%prog [options]" + " - notification gateway"
parser = OptionParser(usage=usage)

#options

parser.add_option("-m", "--metadata", help="Tell daddy what is playing right now", default=False, action="store_true", dest="metadata")
parser.add_option("-t", "--testing", help="Testing...", default=False, action="store_true", dest="testing")
parser.add_option("-C", "--channel", help="Tell daddy what is playing right now", metavar="channel")
parser.add_option("-T", "--title", help="Tell daddy what is playing right now", metavar="title")
parser.add_option("-c", "--channels", help="Update channels file", default=False, action="store_true", dest="channels")
parser.add_option("-d", "--dev", help="Development mode, use dev config", default=False, action="store_true", dest="dev")

# parse options
(options, args) = parser.parse_args()

# configure logging
logging.config.fileConfig("logging.cfg")

# loading config file
try:
    config = ConfigObj('config.cfg')
    TMP_DIR = config['tmp_dir']
   
    BASE_URL = config['base_url']
    API_BASE = config['api_base']
    API_KEY = config['api_key']
    
    API_URL = BASE_URL + API_BASE 
    
except Exception, e:
    print 'error: ', e
    sys.exit()
    
    
class Global:
    def __init__(self):
        print
        
    def selfcheck(self):
        
        if os.geteuid() == 0:
            print '#################################################'
            print "DON'T BE ROOT PLEASE!                            "
            print '#################################################'
            #sys.exit(1)
        
            
         

class Notify:
    
    def __init__(self):

        self.tmp_dir = TMP_DIR 
        
        self.api_key = API_KEY
        self.api_client = ApiClient(API_URL, self.api_key, None)


    def testing(self, options):
        
        print "testing..."
        
        api = slumber.API(API_ENDPOINT, auth=API_AUTH)  
        
        # initial post
        post = api.playout.post({'title': 'my file'})
        print post
    
        # do some seconds of recording, then
        time.sleep(1)
        
        print 'putting sample...'
        # put recorded sample
        put = api.playout(post["id"]).put({'sample': open('samples/cos.mp3')})    
        print put
        
        
    def channels(self, options):
        
        text_file = open(CHANNELS_FILE, "w")
        
        api = slumber.API(API_ENDPOINT, auth=API_AUTH)
        channels = api.channel.get()
        
        # print channels
        
        for channel in channels['objects']:

            if channel['enable_monitoring'] and channel['type'] == 'stream':
            
                channel_id = channel['id']
                stream_url = channel['stream_url']
                channel_name = channel['name']
                
                text_file.write("# Channel: %s \n" % channel_name)
                text_file.write("l%s = input.http(id='inl%s',poll_delay=5.,autostart=true,'%s')\n" % (channel_id, channel_id, stream_url))
                text_file.write("l%s = mksafe(l%s)\n" % (channel_id, channel_id))
                text_file.write("l%s = rewrite_metadata(insert_missing=true,[(\"channel\",\"%s\")],l%s)\n" % (channel_id, channel_id, channel_id))
                text_file.write("l%s = on_metadata(id='ml%s',notify, l%s)\n" % (channel_id, channel_id, channel_id))
                text_file.write("output.dummy(l%s)\n" % (channel_id))
                text_file.write("l%ssample = output.file.wav(id='l%srec',start=false,'samples/l%ssample.wav', l%s)\n" % (channel_id, channel_id, channel_id, channel_id))
                text_file.write("\n\n\n")

            
        
        
        
        text_file.close()
        
        print 'doine'
        
        
        
    def metadata(self, options):
        
        # dev
        #if options.dev:
        #    API_ENDPOINT = 'http://localhost:8000/api/v1/'
        #    API_AUTH = ("root", "root")
        
        do_record = True
        
        api = slumber.API(API_ENDPOINT, auth=API_AUTH) 


        print 'Channel:',
        print options.channel
        print 'String:', 
        print options.title
        print
        
        if not options.title or len(options.title) < 2:
            print 'No title set or title too short... > Exit'
            sys.exit()
            
        # get channel data from API
        channel = api.channel(int(options.channel)).get()
        
        channel_id = channel['id']        
        exclude_list = channel['exclude_list']
        title_only_list = channel['title_only_list']
        
        if len(exclude_list) > 3:

            exclude_list = exclude_list.split(',')
            for e in exclude_list:
                #print '*%s*' % e.strip()
                if e.strip().lower() in options.title.lower():
                    print 'Excluded, as contains: %s' % e
                    sys.exit()
        
        if len(title_only_list) > 3:

            title_only_list = title_only_list.split(',')
            for t in title_only_list:
                #print '*%s*' % t.strip()
                if t.strip().lower() in options.title.lower():
                    print 'Title only, as contains: %s' % t
                    do_record = False
    

        

        # Notify the API
        if not do_record:
            post = api.playout.post({'title': options.title, 'channel': options.channel, 'status': 1})
            sys.exit()
         
        
        # initial post
        post = api.playout.post({'title': options.title, 'channel': options.channel})
        print post
        
        
        # wait a bit befor recording
        print 'sleeping for %s secs' % REC_OFFSET
        time.sleep(REC_OFFSET)
        
        """"""
        tn = telnetlib.Telnet('127.0.0.1', 1234)
        tn.write(("l%srec.start" % channel_id).encode('latin-1'))
        tn.write("\n")
        tn.write("exit\n")
        

        print 'recording for %s secs' % REC_DURATION
        for i in range(REC_DURATION):
            time.sleep(1)
            print "%s " % (REC_DURATION - i),
            sys.stdout.flush()
        print 
        
        """"""
        tn = telnetlib.Telnet('127.0.0.1', 1234)        
        tn.write(("l%srec.stop" % channel_id).encode('latin-1'))
        tn.write("\n")
        tn.write("exit\n")
        
        
        print "*** RECORDING DONE ***"
        
        sample_path = 'samples/l%ssample.wav' % channel_id
        sample_path_mp3 = 'samples/l%ssample.mp3' % channel_id
        
        # lame it..
        p = subprocess.Popen([
            'lame', sample_path, sample_path_mp3,
        ], stdout=subprocess.PIPE)
        stdout = p.communicate() 
        d = stdout[0]
        
        print d
        

        print 'Putting sample: %s' % sample_path_mp3
        # put recorded sample
        try:
            put = api.playout(post["id"]).put({'status': 2, 'sample': open(sample_path_mp3)})    
            print put
        except Exception, e:
            print '************************************************'
            print e
        
        sys.exit()    
    
     
            

if __name__ == '__main__':
  
    # initialize
    g = Global()
    #g.selfcheck()
    n = Notify()


run = True
while run == True:
    
    logger = logging.getLogger("bcmon notify")
            
    if options.testing:
        try: n.testing(options)
        except Exception, e:
            print e
        sys.exit()  
            
    if options.channels:
        try: n.channels(options)
        except Exception, e:
            print e
        sys.exit()  
            
    if options.metadata:
        n.metadata(options)
        try: n.metadata(options)
        except Exception, e:
            print e
        sys.exit()  


    sys.exit()
