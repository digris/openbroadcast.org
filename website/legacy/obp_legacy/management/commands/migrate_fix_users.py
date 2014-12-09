#-*- coding: utf-8 -*-
from optparse import make_option

from django.core.management.base import BaseCommand, NoArgsCommand
from django.conf import settings
from django.db.models import F, Q

#from alibrary.models import Artist, Release, Media, Label, Relation, License

from filer.models.filemodels import File
from filer.models.audiomodels import Audio
from filer.models.imagemodels import Image



from datetime import datetime

from lib.util import filer_extra

DEFAULT_LIMIT = 100
FORCE_UPDATE = True


class Worker(object):

    def __init__(self, * args, **kwargs):
        self.limit = kwargs.get('limit')


    def run(self):
        """
        fixes objects with no user assigned.
        this happened because a bug on the legacy system, which did not assign users at all.
        """

        from alibrary.models import Release
        from profiles.models import Profile
        from obp_legacy.models import Releases

        """
        get releases with legacy id but no 'creator'
        """
        releases_to_fix = Release.objects.exclude(legacy_id=None).filter(creator=None)[0:self.limit]

        print 'num objects to fix: %s' % releases_to_fix.count()

        for release_to_fix in releases_to_fix:
            try:
                legacy_release = Releases.objects.using('legacy').get(id=release_to_fix.legacy_id)
            except:
                legacy_release = None


            if legacy_release and legacy_release.owner:

                try:
                    profile = Profile.objects.get(legacy_legacy_id=legacy_release.owner)
                    user = profile.user
                except Exception, e:
                    print 'profile does not exist: %s' % e
                    user = None

                if not user:
                    print 'unable to find matching user'
                else:
                    print
                    print 'Release'
                    print 'id: %s | legacy_id: %s \t\t  %s' % (release_to_fix.pk, release_to_fix.legacy_id, release_to_fix.name)
                    print 'Legacy Release'
                    print 'owner: %s | user_id: %s' % (legacy_release.owner, legacy_release.user_id)
                    print 'user: %s | %s' % (user.username, user.email)

                    release_to_fix.creator = user
                    release_to_fix.save()










class Command(NoArgsCommand):
    """
    Import directory structure into alibrary:

        manage.py import_folder --path=/tmp/assets/images
    """

    option_list = BaseCommand.option_list + (
        make_option('--limit',
            action='store',
            dest='limit',
            default=DEFAULT_LIMIT,
            help='How many rows to process... defaults to %s' % DEFAULT_LIMIT),
        )

    def handle_noargs(self, **options):
        w = Worker(**options)
        w.run()
