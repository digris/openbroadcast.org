#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import datetime
import re

from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _
from django_extensions.db.fields import *
from django_extensions.db.fields.json import JSONField

from cms.models import CMSPlugin
from alibrary.models import Media
from ep.API import fp


def filename_by_uuid(instance, filename):
    filename, extension = os.path.splitext(filename)
    path = "media/samples/"
    
    # plain
    filename = instance.uuid + extension
    
    # splitted
    #filename = instance.uuid.replace('-', '/') + extension
    
    # timestamped
    filename = datetime.datetime.now().strftime("%Y/%m/%d/") + filename
    
    return os.path.join(path, filename)



class BaseModel(models.Model):
    
    uuid = UUIDField()
    
    created = CreationDateTimeField()
    updated = ModificationDateTimeField()
    
    class Meta:
        abstract = True


class Playout(BaseModel):

    title = models.CharField(max_length=512, null=False, blank=True)
    channel = models.ForeignKey('Channel', null=True, blank=True, on_delete=models.SET_NULL)
    
    meta_name = models.CharField(max_length=512, null=False, blank=True)
    meta_artist = models.CharField(max_length=512, null=False, blank=True)
    
    
    dummy_result = models.CharField(max_length=512, null=False, blank=True)
    
    time_start = models.DateTimeField(null=True, blank=True)
    time_end = models.DateTimeField(null=True, blank=True)
    
    STATUS_CHOICES = (
        (0, _('Waiting')),
        (1, _('Done')),
        (2, _('Ready')),
        (3, _('Error')),
        (4, _('Echoprint directly (no sample)')),
    )
    
    status = models.PositiveIntegerField(default=0, choices=STATUS_CHOICES)
    
    score = models.PositiveIntegerField(default=0)
    
    #sample = models.FileField(upload_to="media/samples/", null=True, blank=True)
    sample = models.FileField(upload_to=filename_by_uuid, null=True, blank=True)
    
    analyzer_data = JSONField(blank=True, null=True)
    enmfp = JSONField(blank=True, null=True)
    echoprint_data = JSONField(blank=True, null=True)
    echoprintfp = JSONField(blank=True, null=True)
    
    # reference to actual media object
    media = models.ForeignKey(Media, null=True, blank=True, on_delete=models.SET_NULL)
    
    
    # meta
    class Meta:
        app_label = 'bcmon'
        verbose_name = _('Playout')
        verbose_name_plural = _('Playouts')
        ordering = ('-created', )

    def __unicode__(self):
        return "%s" % self.title

    @models.permalink
    def get_absolute_url(self):
        return ('bcmon-playout-detail', [self.pk])
    
    def extract_meta(self):
        title_format = self.channel.title_format
        title_format = r"%s" % title_format

        try:
            pattern = re.compile(title_format, re.UNICODE)
            s = self.title
            m = pattern.search(s)
            self.meta_name = m.group('track').strip()
            self.meta_artist = m.group('artist').strip()
            
            
        except Exception, e:
            print e
            pass
    
    def analyze(self):
        
        from lib.analyzer.base import Analyze
        
        a = Analyze()
        
        code, version, enmfp = a.enmfp_from_path(self.sample.path)
        res = a.get_by_enmfp(code, version)
        
        self.enmfp = enmfp
        
        return res
    
    def echoprint(self):
        
        from lib.analyzer.echoprint import Echoprint
        e = Echoprint()
        code, version, duration, echoprint = e.echoprint_from_path(self.sample.path)
        res = e.get_by_echoprintfp(code, version)
        
        self.echoprintfp = echoprint
        return res
    
    def save(self, *args, **kwargs):
        
        if not self.id:
            self.time_start = datetime.datetime.today()
            

        # set time_end for previous entry


        self.extract_meta()
        super(Playout, self).save(*args, **kwargs)
   
   
def playout_post_save(sender, **kwargs):
    
    obj = kwargs['instance']
    
    
    try:
        lps = Playout.objects.filter(channel=obj.channel, time_end=None, status=1).order_by('-created')[1:]
        for lp in lps:
            if lp != obj:
                print lp
                lp.time_end = obj.time_start
                lp.save()
    except Exception, e:
        print e
        pass
    
    
    if (obj.sample and obj.status == '2') or (obj.sample and obj.status == 2):
        
        print 'ready for fingerprinting...'
        
        try:
            obj.analyzer_data = obj.analyze()
            obj.status = 1
            obj.save()
            
        except Exception, e:
            print e
            pass
        
        try:
            res = obj.echoprint()
            
            obj.echoprint_data = {'track_id': res['track_id'], 'score': res['score']}
            
            obj.save()
            
        except Exception, e:
            print e
            pass
        
        
    m = None
        
    if obj.status == '4' or obj.status == 4:
        print 'pre fingerprinted entry'
        code = obj.echoprintfp['code']
        print 'pre q'
        res = fp.best_match_for_query(code_string=code)
        print 'post q'
        
        print res.match()
        if res.match():
        
            print res.message()
            print res.score
            print res.TRID
            
            obj.dummy_result = res.TRID
            
            if res.TRID:
                try:
                    id = int(res.TRID)
                    m = Media.objects.get(pk=id)
                    print m
                    
                    obj.dummy_result = "%s : !! %s" % (m.name, res.score)
                    
                    
                    # other dummy
                    try:
                        obj.dummy_result = "%s:::%s" % (m.name, m.artist.name)
                    except:
                        obj.dummy_result = "%s:::%s" % (m.name, 'Unknown')
                    
                    obj.score = res.score
                    
                    
                except Exception, e:
                    print e
                    pass
            
        else:
            print 
            print    
            print "####### TRYING FOR LOOSE MATCHES..."
    
            try:
                code = fp.decode_code_string(code)
                res = fp.query_fp(code)
                
                print res.results
                
                print 'choosen:'
                print res.results[0]
                
                id = res.results[0]['track_id']
                score = res.results[0]['score']
                m = Media.objects.get(pk=id)
                print m
                
                if score > 50:
                
                    obj.dummy_result = "%s : %s" % (m.name, score)

                    try:
                        obj.dummy_result = "%s:::%s" % (m.name, m.artist.name)
                    except:
                        obj.dummy_result = "%s:::%s" % (m.name, 'Unknown')
                    
                    
                else:
                    obj.dummy_result = "%s:::%s" % ('No Match', '')
                    
                obj.score = score
                
            except Exception, e:
                print e
                pass
            
            print
            print
        

        if m:
            obj.media = m
        
        obj.status = 1;
        obj.save()
        print res

    
    
 
post_save.connect(playout_post_save, sender=Playout)    


class Channel(BaseModel):

    name = models.CharField(max_length=256, null=True, blank=True)
    slug = AutoSlugField(populate_from='name')
    

    
    TYPE_CHOICES = (
        ('stream', _('Stream')),
        ('djmon', _('DJ-Monitor')),
    )
    type = models.CharField(verbose_name=_('Type'), max_length=12, default='stream', choices=TYPE_CHOICES)
    
    stream_url = models.CharField(max_length=256, null=True, blank=True)
    title_format = models.CharField(max_length=256, null=True, blank=True, help_text='Regex to match title against. eg "(?P<artist>[\w\s\d +"*ç%&/(),.-;:_]+?)-(?P<track>[\w\s\d +"*ç%&/(),.-;:_]+?)$" to recognize formats like "The Prodigy  (feat. Whomever) - Remix 3000" - (incl. unicode)')
    
    exclude_list = models.TextField(blank=True, null=True, help_text=_('Comma separated, keywords that should completely be ignored.'))
    title_only_list = models.TextField(blank=True, null=True, help_text=_('Comma separated, only track titles but don\' analyze.'))
    
    enable_monitoring = models.BooleanField(default=True)
    
    class Meta:
        app_label = 'bcmon'
        verbose_name = _('Channel')
        verbose_name_plural = _('Channels')
        ordering = ('name', )

    def __unicode__(self):
        return "%s" % self.name

    @models.permalink
    def get_absolute_url(self):
        return ('bcbon-channel-detail', [self.pk])
    
    
    
class ChannelPlugin(CMSPlugin):    
    channel = models.ForeignKey(Channel, related_name='plugins')
    def __unicode__(self):
        return "%s" % self.channel.name
