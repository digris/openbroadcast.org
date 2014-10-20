#-*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand


class LibDebug(object):
    def __init__(self, * args, **kwargs):
        self.verbosity = int(kwargs.get('verbosity', 1))

    def test_relations(self):
        
        from alibrary.models import Release
        print "test_relations"
        
        r = Release.objects.get(pk=48)
        print r
        
        for rel in r.relations.all():
            print '*****************'
            print 'url:     %s' % rel.url
            print 'service: %s' % rel._service

    def greate_statistics(self):

        media_id = 13334
        num_entries = 500
        user_id = 1


        from datetime import datetime
        import random
        from random import randint
        from alibrary.models import Media
        from atracker.models import Event, EventType
        from django.contrib.auth.models import User

        print "test_relations"

        m = Media.objects.get(pk=media_id)

        for x in range(0, num_entries):


            try:
                et = EventType.objects.order_by('?').all()[0]
                #et = EventType.objects.get(title='stream')
                e = Event.create_event(user=User.objects.order_by('?').all()[0], content_object=m, event_type=et)
                year = random.choice(range(2013, 2015))
                month = random.choice(range(0, 13))
                day = random.choice(range(1, 28))
                hour = random.choice(range(0, 24))
                minute = random.choice(range(0, 60))
                second = random.choice(range(0, 60))
                e.created = datetime(year, month, day, hour, minute, second)
                e.save()
            except Exception, e:
                print e
                pass


            


class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        lib_debug = LibDebug(**options)
        #lib_debug.test_relations()
        lib_debug.greate_statistics()
