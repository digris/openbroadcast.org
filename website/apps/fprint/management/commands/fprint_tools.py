#-*- coding: utf-8 -*-
import sys
import struct
import subprocess
from optparse import make_option

import requests
from django.core.management.base import BaseCommand, NoArgsCommand

import echoprint
from ep.API import fp

REC_DURATION = 30


class FPWorker(object):
    def __init__(self, *args, **kwargs):
        self.action = None
        self.path = kwargs.get('path', None)
        self.lookup = kwargs.get('lookup', None)

        if kwargs.get('codegen'):
            self.action = 'codegen'


        self.verbosity = int(kwargs.get('verbosity', 1))

    def run(self):

        if self.action == 'codegen':
            self.codegen()


    def codegen(self):

        print
        print '#####################################################'
        print 'codegen'
        print 'path: %s' % self.path

        try:
           with open(self.path) as f:
               pass
        except IOError as e:
            print "Unable to open file"
            print e
            sys.exit(1)

        print
        print '#####################################################'
        print 'calling ffmpeg'

        p = subprocess.Popen([
            'ffmpeg',
            '-i', self.path,
            '-ac', '1',
            '-ar', '11025',
            '-f', 's16le',
            '-t', '%s' % (REC_DURATION),
            '-ss', '1',
            '-',
        ], stdout=subprocess.PIPE)

        samples = []

        while True:
            sample = p.stdout.read(2)
            if sample == '':
                break
            samples.append(struct.unpack('h', sample)[0] / 32768.0)

        print
        print '#####################################################'
        print 'Some samples (first 10)'
        print samples[0:10]

        data = echoprint.codegen(samples)
        print
        print '#####################################################'
        print 'generated codestring'

        code = data['code']
        print '# code sequence'
        print fp.decode_code_string(code)

        print '# code string'
        print code
        print data['version']

        # calling api...
        if self.lookup:
            print
            print '#####################################################'
            print 'API SAYS...'
            r = requests.get("http://local.openbroadcast.org:8080/en/api/v1/library/track/?format=json&code=%s" % code)
            res = r.json()

            print res

            print
            print res['objects'][0]['absolute_url']



class Command(NoArgsCommand):

    option_list = BaseCommand.option_list + (
        make_option('--codegen',
                    action='store_true',
                    dest='codegen',
                    default=None,
                    help='generate fingerprint'),
        make_option('--lookup',
                    action='store_true',
                    dest='lookup',
                    default=None,
                    help='alos do api lookup for code'),
        make_option('--path',
                    action='store',
                    dest='path',
                    default=None,
                    help='File path'),
    )

    def handle_noargs(self, **options):
        worker = FPWorker(**options)
        worker.run()
