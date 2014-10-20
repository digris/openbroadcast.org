import os
from optparse import make_option

from django.core.files.storage import FileSystemStorage
from django.core.management.base import NoArgsCommand
from django.contrib.staticfiles import finders, storage
from django.template.loader import render_to_string


from nunjucks.compiler import NunjucksCompiler




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
        target = 'apps/nunjucks/static/nunjucks/js/templates.js'
        templates = []
        for finder in finders.get_finders():
            for path, storage in finder.list(['*zinnia*']):

                if getattr(storage, 'prefix', None):
                    prefixed_path = os.path.join(storage.prefix, path)
                else:
                    prefixed_path = path

                # TOTO: find a correct way to get nj-paths
                if '/nj/' in path:
                    templates.append( {
                        'path': path,
                        'inner': self.compiler.compile(storage.path(path))
                        }
                    )


        tpl = render_to_string('nunjucks/compile/templates.js', {'templates': templates})

        open(target, "w").write(tpl)

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





    def compile_file(self, path, prefixed_path, source_storage):

        # dummy, to test compiler


        source_path = source_storage.path(path)

        if 'on_air_item.html' in path:


            print
            print 'path:           %s' % path
            print 'prefixed_path:  %s' % prefixed_path
            print 'source_path:    %s' % source_path
            print 'source_storage: %s' % source_storage


            print self.compiler.compile(source_path)




    def copy_file(self, path, prefixed_path, source_storage):
        """
        Attempt to copy ``path`` with storage
        """
        # Skip this file if it was already copied earlier
        if prefixed_path in self.copied_files:
            return self.log("Skipping '%s' (already copied earlier)" % path)
        # Delete the target file if needed or break
        if not self.delete_file(path, prefixed_path, source_storage):
            return
        # The full path of the source file
        source_path = source_storage.path(path)
        # Finally start copying
        if self.dry_run:
            self.log("Pretending to copy '%s'" % source_path, level=1)
        else:
            self.log("Copying '%s'" % source_path, level=1)
            if self.local:
                full_path = self.storage.path(prefixed_path)
                try:
                    os.makedirs(os.path.dirname(full_path))
                except OSError:
                    pass
            with source_storage.open(path) as source_file:
                self.storage.save(prefixed_path, source_file)
        if not prefixed_path in self.copied_files:
            self.copied_files.append(prefixed_path)