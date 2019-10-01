# -*- coding: utf-8 -*-
from __future__ import absolute_import
import subprocess
import logging

from nunjucks import settings as nunjucks_settings

log = logging.getLogger(__name__)


class NunjucksCompiler(object):
    def __init__(self):
        pass

    def compile_template(self, path):

        template = ""
        command = "%s %s" % (nunjucks_settings.NUNJUCKS_BIN, path)

        p = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        for line in p.stdout.readlines():
            template += line
        retval = p.wait()

        return template
