#-*- coding: utf-8 -*-
from optparse import make_option
import time
import json
import random

from django.core.management.base import BaseCommand, NoArgsCommand
import redis
import requests

from alibrary.models import Media


class Pusher(object):
    
    def __init__(self, * args, **kwargs):
        self.verbosity = int(kwargs.get('verbosity', 1))
        
        self.redis = redis.StrictRedis()
        
        
    def push_forever(self):
        while True:
            self.push_dummy()
            time.sleep(random.randint(1,15))
        
        

    def push_dummy(self):
        
        print "#########################"
        print "push_dummy"
        print "#########################"
        
        #m = Media.objects.get(pk=16624)
        #m = Media.objects.order_by('?')[0]
        m = Media.objects.exclude(release__main_image=None).order_by('?')[0]
        
        print m.get_api_url()
        
        #r = requests.get('http://dev.openbroadcast.org/de%s?format=json' %  m.get_api_url())
        r = requests.get('http://localhost:8080/de%s?format=json' %  m.get_api_url())
        #print r.json
        
        
        data = {'type': '%s' % 'media', 'user': '%s' % 'none', 'object': r.json}
        
        self.redis.publish('push_chat', json.dumps(data))
        

        




class Command(NoArgsCommand):
    
    option_list = BaseCommand.option_list + (
        make_option('--path',
            action='store',
            dest='path',
            default=False,
            help='Import files located in the path into django-filer'),
        )

    def handle_noargs(self, **options):
        pusher = Pusher(**options)
        pusher.push_forever()
