
import subprocess
import json
import logging
from django.conf import settings

log = logging.getLogger(__name__)

ECHOPRINT_CODEGEN_BINARY = getattr(settings, 'ECHOPRINT_CODEGEN_BINARY', 'echoprint-codegen')
ECHOPRINT_DEFAULT_OFFSET = 10
ECHOPRINT_DEFAULT_DURATION = 100

class Echoprint:

    def echoprint_from_path(self, path, offset=None, duration=None):

        log.debug('echoprint binary: %s' % ECHOPRINT_CODEGEN_BINARY)

        offset = offset or ECHOPRINT_DEFAULT_OFFSET
        duration = duration or ECHOPRINT_DEFAULT_DURATION

        p = subprocess.Popen([
            ECHOPRINT_CODEGEN_BINARY, path, '%s' % offset, '%s' % (offset + duration)
        ], stdout=subprocess.PIPE)
        stdout = p.communicate()
        echoprint_data = json.loads(stdout[0])

        code = None
        version = None
        try:
            code = echoprint_data[0]['code']
            version = echoprint_data[0]['metadata']['version']
            duration = echoprint_data[0]['metadata']['duration']

            log.info(u'echoprint result - version: %s - duration: %s' % (version, duration))

        except IndexError as e:
            log.warning(u'unable to generate echoprint: %s' % e)
            pass

        return code, version, duration, echoprint_data


def echoprint_from_path(path, offset=None, duration=None):
    ep = Echoprint()
    code, version, duration, echoprint = ep.echoprint_from_path(path, offset=offset, duration=duration)

    return code, version, duration, echoprint



