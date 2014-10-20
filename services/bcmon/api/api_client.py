#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author Jonas Ohrstrom <jonas@digris.ch>

import sys
import time
import urllib
import commands
import socket

#from util import urllib2_file
import urllib2

import logging

from util import json

import os


        
class ApiClient():

    def __init__(self, api_url, api_key, target):
        self.api_url = api_url
        self.api_key = api_key
        self.target = target

    def get_version(self):
        logger = logging.getLogger("ApiClient.get_version")
        # lookup OBP version
        
        url = self.api_url + 'status.json'
        data = urllib.urlencode({'apikey': self.api_key})

        logger.debug("%s", url)
        
        try:
            
            logger.debug("Trying to contact %s", url)
            
            response = urllib.urlopen(url, data)
            response_json = json.read(response.read())
            api_version = int(response_json['api_version'])
            max_upload = int(response_json['max_upload'])
            logger.debug("API Version %s detected", api_version)

    
        except Exception, e:
            try:
                if e[1] == 401:
                    print '#####################################'
                    print '# YOUR API KEY SEEMS TO BE INVALID'
                    print '# ' + self.api_key
                    print '#####################################'
                    logger.critical("API Key invalid")
                    #sys.exit()
                    #time.sleep(30)
                    
            except Exception, e:
                pass
            
            try:
                if e[1] == 404:
                    print '#####################################'
                    print '# Unable to contact the OBP-API'
                    print '# ' + url
                    print '#####################################'
                    logger.critical("Unable to connect to API at %s", url)
                    #sys.exit()
                    #time.sleep(30)
                    
            except Exception, e:
                pass
            
            api_version = 0
            max_upload = 0
            logger.error("Unable to detect API Version - %s", e)

        
        return api_version, max_upload


    
    
    def metadata_change(self, station, title):
        
        logger = logging.getLogger("ApiClient.metadata_change")
        
        
        data = {'apikey': self.api_key, 'station': station, 'title': title}
        
        url = self.api_url + 'metadata_change.json' 
        data = urllib.urlencode(data)
        
        logger.debug("%s", url)
        
        try:
            logger.debug("Trying to contact %s", url)
            response = urllib.urlopen(url, data)
            response_json = json.read(response.read())
            
            api_version = int(response_json['api_version'])

            print response_json

            status = True

        except Exception, e:
            #print e
            status = False
            
        
        return status
    

    
    

    
    


    
    