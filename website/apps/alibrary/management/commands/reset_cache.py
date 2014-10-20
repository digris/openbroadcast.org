#-*- coding: utf-8 -*-
#from django.core.files import File as DjangoFile
import os
from optparse import make_option

from django.core.management.base import BaseCommand, NoArgsCommand

from cms.models import CMSPlugin
from alibrary.models import *


class CacheReset(object):
    def __init__(self, * args, **kwargs):
        self.filter_by = kwargs.get('filter_by')
        self.verbosity = int(kwargs.get('verbosity', 1))

        try:
            self.filter_by = self.filter_by.split('=')

        except Exception, e:
            self.filter_by = False

    def test(self):
        if self.filter_by:
            objs = Media.objects.filter(self.filter_by)
        else:
            objs = Media.objects.all()
        
        for obj in objs:
            print obj.uuid,
            print ' | ',
            print obj.name

    def reset(self):
        if self.filter_by:
            objs = Media.objects.filter(self.filter_by)
        else:
            objs = Media.objects.all()
        
        for obj in objs:
            
            print obj.uuid,
            print ' | ',
            print obj.name
            
            obj.processed = 0
            obj.save()

        """
        objs = Media.objects.all()
        for obj in objs:
            print 'DELETE:', 
            print obj.name
            # recreate cache
            obj.convert.delay(obj, 'wav', 'base') 
            obj.convert.delay(obj, 'flac', 'base') 
            obj.convert.delay(obj, 'mp3', 'base') 
        """

    def reset__old(self):
        if self.filter_by:
            objs = Media.objects.filter(self.filter_by)
        else:
            objs = Media.objects.all()
        
        for obj in objs:
            
            print obj.uuid,
            print ' | ',
            print obj.name
            
            obj.processed = 0
            obj.save()
            
            try:
                if obj.folder:
                    for file in obj.folder.files:
                        print file.path
                        os.remove(file.path)
                        file.delete()
                    
            except Exception, e:
                print e
                
        objs = Media.objects.all()
        for obj in objs:
            print 'DELETE:', 
            print obj.name
            # recreate cache
            obj.convert.delay(obj, 'wav', 'base') 
            obj.convert.delay(obj, 'flac', 'base') 
            obj.convert.delay(obj, 'mp3', 'base') 


class Command(NoArgsCommand):

    option_list = BaseCommand.option_list + (
        make_option('--filter',
            action='store',
            dest='filter_by',
            default=False,
            help='Filter criterias for reset'),
        )

    def handle_noargs(self, **options):
        
        cache_reset = CacheReset(**options)
        # cache_reset.test()
        cache_reset.reset()
