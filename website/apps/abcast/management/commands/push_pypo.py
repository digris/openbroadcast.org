#-*- coding: utf-8 -*-
from optparse import make_option
import datetime
from django.core.management.base import BaseCommand, NoArgsCommand
from django.utils import translation

from lib.pypo_gateway import PypoGateway
from lib.pypo_gateway import send as pypo_send
from abcast.util import scheduler



class Pusher(object):
    def __init__(self, * args, **kwargs):
        self.action = kwargs.get('action')
        self.message = kwargs.get('message')
        self.verbosity = int(kwargs.get('verbosity', 1))
        
    def run(self):

        translation.activate('en')

        if self.action == 'update_schedule':

            range_start = datetime.datetime.now()
            range_end = datetime.datetime.now() + datetime.timedelta(seconds=60*60*6)
            data = scheduler.get_schedule_for_pypo(range_start, range_end)

            pg = PypoGateway()
            message = {
                'event_type': 'update_schedule',
                'schedule': {'media': data},
            }
            pg.send(message)

        if self.action == 'reset_schedule':

            message = {
                'event_type': 'update_schedule',
                'schedule': {'media': []},
            }
            pypo_send(message)

        if self.action == 'custom_message':

            message = {
                'event_type': '%s' % self.message,
                'schedule': {'media': []},
            }
            pypo_send(message)



class Command(NoArgsCommand):

    option_list = BaseCommand.option_list + (
        make_option('--action',
            action='store',
            dest='action',
            default=False,
            help='Fill up the scheduler!!'),
        make_option('--message',
            action='store',
            dest='message',
            default=False,
            help='Fill up the scheduler!!'),
        )

    def handle_noargs(self, **options):
        p = Pusher(**options)
        p.run()
