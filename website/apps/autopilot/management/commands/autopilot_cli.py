#-*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import argparse
import textwrap
from django.core.management.base import BaseCommand
from django.conf import settings
from autopilot.util import Autopilot

log = logging.getLogger(__name__)

DEFAULT_CHANNEL_ID = getattr(settings, 'AUTOPILOT_DEFAULT_CHANNEL_ID', 1)
DEFAULT_USERNAME = getattr(settings, 'AUTOPILOT_DEFAULT_USERNAME', 'autopilot')
NUM_DAYS = 1
NUM_DAYS_OFFSET = 0
DEFAULT_THEME = 3


COMMAND_DESCRIPTION = ''''''
COMMAND_EXAMPLE = '''\
Example uf use:
--------------------------

    python manage.py autopilot_cli schedule -c 1 -u peter

.
'''


class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.formatter_class=argparse.RawDescriptionHelpFormatter
        #parser.description=textwrap.dedent(COMMAND_DESCRIPTION)
        parser.epilog=textwrap.dedent(COMMAND_EXAMPLE)

        parser.add_argument(
                'action',
                type=str,
                choices=[
                    'schedule',
                    'reset',
                    'test_slots',
                ]
        )

        parser.add_argument('-c', '--channel',
            action='store',
            type=int,
            dest='channel_id',
            default=DEFAULT_CHANNEL_ID,
            help='Channel ID [{:}]'.format(DEFAULT_CHANNEL_ID)
        )

        parser.add_argument('-u', '--username',
            action='store',
            dest='username',
            default=DEFAULT_USERNAME,
            help='Username to schedule in name of [{:}]'.format(DEFAULT_USERNAME)
        )

        parser.add_argument('-o', '--days_offset',
            action='store',
            type=int,
            dest='days_offset',
            default=NUM_DAYS_OFFSET,
            help='Days in future to start. 0 = "today" [{:}]'.format(NUM_DAYS_OFFSET)
        )

        parser.add_argument('-d', '--days_fill',
            action='store',
            type=int,
            dest='days_fill',
            default=NUM_DAYS,
            help='Number of days to schedule ahead [{:}]'.format(NUM_DAYS)
        )

        parser.add_argument('--force',
            action='store_true',
            dest='force',
            help='Force action. No prompt will be displayed.'
        )


    def handle(self, *args, **options):

        self.stdout.write('\n\n\nRunning Autopilot')


        # self.stdout.write('Running Autopilot with:')
        # for k, v in options.iteritems():
        #     self.stdout.write('{:14s}: {:}'.format(k, v))

        ap = Autopilot(
                channel_id=options['channel_id'],
                username=options['username'],
        )

        ap_action = getattr(ap, options['action'])
        ap_action(
                days_offset=options['days_offset'],
                days_fill=options['days_fill'],
        )
