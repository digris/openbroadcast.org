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


"""

# python defaults (debian default)
import time
import os
import traceback
from optparse import OptionParser
import sys
import time
import datetime
import logging
import logging.config
import urllib
import urllib2
import string

# additional modules (should be checked)
from configobj import ConfigObj

# custom imports
from util import *
from api import *
#from dls import *



BCMON_VERSION = '0.1'
API_MIN_VERSION = 20110201 # required obp version


#set up command-line options
parser = OptionParser()

# help screeen / info
usage = "%prog [options]" + " - notification gateway"
parser = OptionParser(usage=usage)

#options

parser.add_option("-m", "--metadata", help="Tell daddy what is playing right now", default=False, action="store_true", dest="metadata")
parser.add_option("-C", "--channel", help="Tell daddy what is playing right now", metavar="channel")
parser.add_option("-T", "--title", help="Tell daddy what is playing right now", metavar="title")

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
        
        self.api_key = API_KEY
        self.api_client = ApiClient(API_URL, self.api_key, None)
        
        if os.geteuid() == 0:
            print '#################################################'
            print "DON'T BE ROOT PLEASE!                            "
            print '#################################################'
            #sys.exit(1)
        
        api_version, max_upload = self.api_client.get_version()
        
        if api_version == 0:
            print '#################################################'
            print 'Unable to get API version. Plattform running?'
            print '#################################################'
            print
            sys.exit()
         
        elif api_version < API_MIN_VERSION:
            print 'API version: ' + str(api_version)
            print 'API min-version: ' + str(API_MIN_VERSION)
            print 'pyar not compatible with this API-Version'
            print
            sys.exit()
         
        else:
            print 'API: ' + str(API_BASE)
            print 'API-version: ' + str(api_version)
            #print 'OBP min-version: ' + str(API_MIN_VERSION)
            #print 'pyar is compatible with this API-Version'
            print
            
         

class Notify:
    def __init__(self):

        self.tmp_dir = TMP_DIR 
        
        self.api_key = API_KEY
        self.api_client = ApiClient(API_URL, self.api_key, None)


    
    def metadata(self, options):
        logger = logging.getLogger("monitoring")

        print 'Channel:',
        print options.channel
        print 'String:', 
        print options.title
        print

        # Notify the API
        try:
            if len(options.title) > 0:
                logger.info("%s: %s", options.channel, options.title)
                
                try:
                    print 'API CONTACT'

                    self.api_client.metadata_change(options.channel, options.title)
                    
                except Exception, e:
                    print e    
                
            else:
                print 'string to short - metadata error'

        except Exception, e:
            print e
   
        
        sys.exit()  

        

     
            

if __name__ == '__main__':
  
    # initialize
    g = Global()
    g.selfcheck()
    n = Notify()


run = True
while run == True:
    
    logger = logging.getLogger("bcmon notify")
            
    if options.metadata:
        try: n.metadata(options)
        except Exception, e:
            print e
        sys.exit()  


    sys.exit()
