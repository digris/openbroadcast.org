#-*- coding: utf-8 -*-
from __future__ import absolute_import
import re
import logging
import codecs
from optparse import make_option
from django.core.files.storage import FileSystemStorage
from django.core.management.base import NoArgsCommand
from django.contrib.staticfiles import finders, storage
from django.template.loader import render_to_string

from nunjucks.compiler import NunjucksCompiler
from nunjucks import settings as nunjucks_settings

log = logging.getLogger(__name__)

class Command(NoArgsCommand):
    """
    Command that allows to copy or symlink static files from different
    locations to the settings.STATIC_ROOT.
    """
    option_list = NoArgsCommand.option_list + (
        make_option('--compile',
            action='store_false', dest='do_compile', default=False,
            help="Compile nunjucks templates"),
        make_option('-n', '--dry-run',
            action='store_true', dest='dry_run', default=False,
            help="Do everything except modify the filesystem."),
    )
    help = "Compile nunjucks templates."
    requires_model_validation = False

    def __init__(self, *args, **kwargs):
        super(NoArgsCommand, self).__init__(*args, **kwargs)
        self.storage = storage.staticfiles_storage
        try:
            self.storage.path('')
        except NotImplementedError:
            self.local = False
        else:
            self.local = True

        self.compiler = NunjucksCompiler()

    def set_options(self, **options):
        self.do_compile = options['do_compile']
        self.dry_run = options['dry_run']

    def collect(self):
        target = 'apps/nunjucks/static/nunjucks/js/compiled-templates.js'
        templates = []
        for finder in finders.get_finders():
            for path, storage in finder.list([]):

                # TOTO: find a correct way to get nj-paths



                if '/nj/' in path:

                    print path
                    print storage.path(path)
                    compiled_template = self.compiler.compile(storage.path(path))

                    print compiled_template

                    compiled_template = re.sub('/Users/ohrstrom/Documents/Code/openbroadcast.org/website/apps/(\w*)/static/', '', compiled_template)


                    #compiled_template = compiled_template.replace('/Users/ohrstrom/Documents/Code/openbroadcast.ch/website/', '')

                    templates.append( {
                        'path': path,
                        'inner': compiled_template
                        }
                    )



        tpl = render_to_string('nunjucks/compile/templates.js', {'templates': templates})
        file = codecs.open(target, "w", "utf-8")
        file.write(tpl)
        file.close()

        return

    def handle_noargs(self, **options):
        self.set_options(**options)
        # Warn before doing anything more.
        if (isinstance(self.storage, FileSystemStorage) and
                self.storage.location):
            destination_path = self.storage.location
            destination_display = ':\n\n    %s' % destination_path
        else:
            destination_path = None
            destination_display = '.'

        collected = self.collect()

