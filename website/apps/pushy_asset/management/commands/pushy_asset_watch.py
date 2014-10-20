import os
from optparse import make_option

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler



from django.core.files.storage import FileSystemStorage
from django.core.management.base import NoArgsCommand
from django.contrib.staticfiles import storage

from pushy_asset.compiler import PushyAssetCompiler




from settings import PROJECT_DIR


class AssetChangedHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print '************** MOD **********'
        from pushy.util import pushy_custom
        pushy_custom('pushy_asset/refresh/', None, 'update')


class Command(NoArgsCommand):
    """
    Command that allows to copy or symlink static files from different
    locations to the settings.STATIC_ROOT.
    """
    option_list = NoArgsCommand.option_list + (
        make_option('--compile',
            action='store_false', dest='do_compile', default=False,
            help="Compile pushy_asset templates"),
        make_option('-n', '--dry-run',
            action='store_true', dest='dry_run', default=False,
            help="Do everything except modify the filesystem."),
    )
    help = "Compile pushy_asset templates."
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

        self.compiler = PushyAssetCompiler()

    def set_options(self, **options):
        self.do_compile = options['do_compile']
        self.dry_run = options['dry_run']

    def watch(self):
        path = os.path.join(PROJECT_DIR, 'site-static', 'css')
        target = 'pushy_asset/refresh/'
        print target
        import logging
        logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
        event_handler = AssetChangedHandler()

        observer = Observer()
        observer.schedule(event_handler, path=path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()



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

        collected = self.watch()

