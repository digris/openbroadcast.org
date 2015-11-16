# -*- coding: utf-8 -*-
from __future__ import with_statement
from contextlib import contextmanager
import os
import requests
from django.conf import settings
from django.utils.decorators import method_decorator
from django.utils.termcolors import colorize


SUCCESS = 1
WARNING = 2
ERROR = 3
SKIPPED = 4

CHECKERS = []


class FileOutputWrapper(object):
    """
    Wraps two file-like objects (that support at the very least the 'write'
    method) into an API to be used by the check function further down in
    this module.

    The following properties are public (and required) by alternative implementations:

        errors: integer count of errors encountered
        successes: integer count of successes encountered
        warnings: integer count of warnings encountered
        skips: integer count of skips encountered
        successful: Whether the checks were successful (no errors)

    They must also provide these methods:

        write_line(message=''): writes a message to stdout
        write_stderr_line(message=''): writes a message to stderr
        success(message): reports and registers a successful check
        error(message): reports and registers an error
        warn(message); reports and registers a warning
        skip(message): reports and registers a skipped check
        section(title): A context manager that starts a new section. For the
            Section API see FileSectionWrapper
    """
    def __init__(self, stdout, stderr):
        self.stdout = stdout
        self.stderr = stderr
        self.section_wrapper = FileSectionWrapper
        self.errors = 0
        self.successes = 0
        self.warnings = 0
        self.skips = 0

    def colorize(self, msg, opts=(), **kwargs):
        return colorize(msg, opts=opts, **kwargs)

    def write_line(self, message=''):
        self.write(u'%s\n' % message)

    def write(self, message):
        self.stdout.write(message)

    def write_stderr_line(self, message=''):
        self.write_stderr(u'%s\n' % message)

    def write_stderr(self, message):
        self.stderr.write(message)

    def success(self, message):
        self.successes += 1
        self.write_line(u'%s %s' % (message, self.colorize('[OK]', fg='green', opts=['bold'])))

    def error(self, message):
        self.errors += 1
        self.write_stderr_line(u'%s %s' % (message, self.colorize('[ERROR]', fg='red', opts=['bold'])))

    def warn(self, message):
        self.warnings += 1
        self.write_stderr_line(u'%s %s' % (message, self.colorize('[WARNING]', fg='yellow', opts=['bold'])))

    def skip(self, message):
        self.skips += 1
        self.write_line(u'%s %s' % (message, self.colorize('[SKIP]', fg='blue', opts=['bold'])))

    @method_decorator(contextmanager)
    def section(self, title):
        self.write_line(self.colorize(title, opts=['bold']))
        self.write_line(self.colorize('=' * len(title), opts=['bold']))
        self.write_line()
        wrapper = self.section_wrapper(self)
        try:
            yield wrapper
        except:
            self.error('Checker failed, see traceback')
            raise
        self.errors += wrapper.errors
        self.successes += wrapper.successes
        self.warnings += wrapper.warnings
        self.skips += wrapper.skips
        self.write_line('')

    @property
    def successful(self):
        return not self.errors


class FileSectionWrapper(FileOutputWrapper):
    """
    Used from FileOutputWrapper to report checks in a section.

    If you want to provide your own output class, you may want to subclass
    this class for the section reporting too. If you want to use your own,
    you must defined at least the same API as FileOutputWrapper, as well
    as these four additional methods:

        finish_success(message): End the section (successfully)
        finish_error(message): End the section with errors
        finish_warning(message): End this section with a warning
        finish_skip(message): End this (skipped) section
    """
    def __init__(self, wrapper):
        super(FileSectionWrapper, self).__init__(wrapper.stdout, wrapper.stderr)
        self.wrapper = wrapper

    def write_line(self, message=''):
        self.write(u'  - %s\n' % message)

    def write_stderr_line(self, message=''):
        self.write_stderr(u'  - %s\n' % message)

    def finish_success(self, message):
        self.wrapper.write_line()
        self.wrapper.success(message)

    def finish_error(self, message):
        self.wrapper.write_line()
        self.wrapper.error(message)

    def finish_warning(self, message):
        self.wrapper.write_line()
        self.wrapper.warning(message)

    def finish_skip(self, message):
        self.wrapper.write_lin()
        self.wrapper.skip(message)


def define_check(func):
    """
    Helper decorator to register a check function.
    """
    CHECKERS.append(func)
    return func


@define_check
def check_binaries(output):

    BINARIES_TO_CHECK = (
        'LAME_BINARY',
        'SOX_BINARY',
        'FAAD_BINARY',
        'FFPROBE_BINARY',
        'ENMFP_CODEGEN_BINARY',
        'ECHOPRINT_CODEGEN_BINARY',
    )

    with output.section("Required binaries") as section:

        for key in BINARIES_TO_CHECK:
            path = getattr(settings, key, None)
            if not path:
                section.error("Settgins for %s binary missing!" % key)

            elif not os.path.isfile(path):
                section.error("%s path does not exist at %s" % (key, path))

            else:
                section.success("%s found: %s" % (key, path))


        if section.successful:
            section.finish_success("Binary configuration okay")
        else:
            section.finish_error("Binary configuration has errors")


@define_check
def check_directories(output):

    with output.section("Directories & storage") as section:

        BASE_DIR = getattr(settings, 'BASE_DIR', None)

        path = os.path.join(BASE_DIR, 'media')
        if not path:
            section.error("Settgins for %s directory missing!" % 'BASE_DIR')

        elif not os.path.isdir(path):
            section.error("%s directory does not exist at %s" % ('BASE_DIR', path))

        else:
            section.success("%s found: %s" % ('BASE_DIR', path))

        if section.successful:
            section.finish_success("Directory configuration okay")
        else:
            section.finish_error("Directory configuration has errors")


@define_check
def check_apis(output):

    with output.section("APIs") as section:

        MUSICBRAINZ_HOST = getattr(settings, 'MUSICBRAINZ_HOST', None)
        host = MUSICBRAINZ_HOST
        if not host:
            section.error("Settgins for %s directory missing!" % 'MUSICBRAINZ_HOST')
        else:
            url = 'http://' + MUSICBRAINZ_HOST + '/ws/2/artist/1582a5b8-538e-45e7-9ae4-4099439a0e79'
            r = requests.get(url)
            if r.status_code == 200:
                section.success("Sucessfully connected to %s - status: %s" % (url, r.status_code))
            else:
                section.error("Unable to connect to %s - status: %s" % (url, r.status_code))





        DISCOGS_HOST = getattr(settings, 'DISCOGS_HOST', None)
        host = DISCOGS_HOST
        if not host:
            section.error("Settgins for %s directory missing!" % 'DISCOGS_HOST')
        else:
            url = 'http://' + DISCOGS_HOST + '/labels/1'
            r = requests.get(url)
            if r.status_code == 200:
                section.success("Sucessfully connected to %s - status: %s" % (url, r.status_code))
            else:
                section.error("Unable to connect to %s - status: %s" % (url, r.status_code))







        if section.successful:
            section.finish_success("Directory configuration okay")
        else:
            section.finish_error("Directory configuration has errors")



def check(output):
    """
    Checks the configuration/environment of this platform installation.

    'output' should be an object that provides the same API as FileOutputWrapper.

    Returns whether the configuration/environment are okay (has no errors)
    """
    title = "Checking Open Broadcast platform installation"
    border = '*' * len(title)
    output.write_line(output.colorize(border, opts=['bold']))
    output.write_line(output.colorize(title, opts=['bold']))
    output.write_line(output.colorize(border, opts=['bold']))
    output.write_line()
    for checker in CHECKERS:
        checker(output)
    output.write_line()
    with output.section("OVERALL RESULTS"):
        if output.errors:
            output.write_stderr_line(output.colorize("%s errors!" % output.errors, opts=['bold'], fg='red'))
        if output.warnings:
            output.write_stderr_line(output.colorize("%s warnings!" % output.warnings, opts=['bold'], fg='yellow'))
        if output.skips:
            output.write_line(output.colorize("%s checks skipped!" % output.skips, opts=['bold'], fg='blue'))
        output.write_line(output.colorize("%s checks successful!" % output.successes, opts=['bold'], fg='green'))
        output.write_line()
        if output.errors:
            output.write_stderr_line(output.colorize('Please check the errors above', opts=['bold'], fg='red'))
        elif output.warnings:
            output.write_stderr_line(output.colorize('Installation okay, but please check warnings above', opts=['bold'], fg='yellow'))
        else:
            output.write_line(output.colorize('Installation seems to be okay', opts=['bold'], fg='green'))
    return output.successful
