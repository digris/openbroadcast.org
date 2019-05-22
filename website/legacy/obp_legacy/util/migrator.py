import os
import re
import time
import shutil
import json
import datetime
import ntpath
from django.core.validators import email_re
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from html2text import html2text
from django.contrib.auth import get_user_model
from tagging.models import Tag
from django.conf import settings


from obp_legacy.models import *


from alibrary.util.storage import get_file_from_path

from l10n.models import Country

LEGACY_STORAGE_ROOT = getattr(settings, 'LEGACY_STORAGE_ROOT', True)
MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', True)

import logging

log = logging.getLogger(__name__)

validate_url = URLValidator()


class Migrator(object):
    pass


class ReleaseMigrator(Migrator):

    def __init__(self):
        log = logging.getLogger('util.migrator.__init__')


    def run(self, legacy_obj, force=False):

        from alibrary.models import Release, Relation

        status = 1

        log = logging.getLogger('util.migrator.run')
        log.info('migrate release: %s' % legacy_obj.name)

        obj, created = Release.objects.get_or_create(legacy_id=legacy_obj.id)

        if created:
            log.info('object created: %s' % obj.pk)
        else:
            log.info('object found by legacy_id: %s' % obj.pk)

        if created or force:
            """
            Mapping data
            1-to-1 fields
            """
            obj.name = legacy_obj.name[:190]
            obj.created = legacy_obj.created
            obj.updated = legacy_obj.updated

            print '*****************************'

            if legacy_obj.catalognumber:
                log.debug('catalognumber: %s' % legacy_obj.catalognumber)
                obj.catalognumber = legacy_obj.catalognumber

            if legacy_obj.releasetype:
                log.debug('releasetype: %s' % legacy_obj.releasetype)
                obj.releasetype = legacy_obj.releasetype

            if legacy_obj.releasestatus:
                obj.releasestatus = legacy_obj.releasestatus

            #if legacy_obj.published:
            #    obj.publish_date = legacy_obj.published

            if legacy_obj.notes:
                obj.description = legacy_obj.notes

            if legacy_obj.totaltracks:
                obj.totaltracks = legacy_obj.totaltracks

            if legacy_obj.releasecountry:
                log.debug('releasecountry: %s' % legacy_obj.releasecountry)
                releasecountry = None
                if len(legacy_obj.releasecountry) == 2:
                    try:
                        releasecountry = Country.objects.get(iso2_code=legacy_obj.releasecountry)
                    except Exception, e:
                        pass

                else:
                    try:
                        releasecountry = Country.objects.get(printable_name=legacy_obj.releasecountry)
                    except Exception, e:
                        pass

                if releasecountry:
                    log.debug('got country: %s' % releasecountry.name)
                    obj.release_country = releasecountry


            if legacy_obj.releasedate:
                log.debug('legacy-date: %s' % legacy_obj.releasedate)
                date = legacy_obj.releasedate
                if len(date) == 4:
                    date = '%s-00-00' % (date)
                elif len(date) == 7:
                    date = '%s-00' % (date)
                elif len(date) == 10:
                    date = '%s' % (date)

                re_date = re.compile('^\d{4}-\d{2}-\d{2}$')
                if re_date.match(date) and date != '0000-00-00':
                    try:
                        import time

                        valid_date = time.strptime('%s' % date, '%Y-%m-%d')
                        obj.releasedate_approx = '%s' % date
                    except Exception, e:
                        print 'Invalid date!'
                        print e

            """
            Relation mapping
            """
            if legacy_obj.discogs_releaseid and legacy_obj.discogs_releaseid != 'nf':
                url = 'http://www.discogs.com/release/%s' % legacy_obj.discogs_releaseid
                log.debug('discogs_url: %s' % url)
                rel = Relation(content_object=obj, url=url)
                rel.save()

            if legacy_obj.mb_releaseid and legacy_obj.mb_releaseid != 'nf':
                url = 'http://musicbrainz.org/release/%s' % legacy_obj.mb_releaseid
                log.debug('mb_releaseid: %s' % url)
                rel = Relation(content_object=obj, url=url)
                rel.save()

            if legacy_obj.myspace_url and legacy_obj.myspace_url != 'nf':
                rel = Relation(content_object=obj, url=legacy_obj.myspace_url)
                log.debug('url: %s' % rel.url)
                rel.save()

            if legacy_obj.wikipedia_url and legacy_obj.wikipedia_url != 'nf':
                rel = Relation(content_object=obj, url=legacy_obj.wikipedia_url)
                log.debug('url: %s' % rel.url)
                rel.save()

            if legacy_obj.facebook_url and legacy_obj.facebook_url != 'nf':
                rel = Relation(content_object=obj, url=legacy_obj.facebook_url)
                log.debug('url: %s' % rel.url)
                rel.save()

            if legacy_obj.lastfm_url and legacy_obj.lastfm_url != 'nf':
                rel = Relation(content_object=obj, url=legacy_obj.lastfm_url)
                log.debug('url: %s' % rel.url)
                rel.save()

            if legacy_obj.release_url and legacy_obj.release_url != 'nf':
                rel = Relation(content_object=obj, url=legacy_obj.release_url, service='official')
                log.debug('url: %s' % rel.url)
                rel.save()

            if legacy_obj.various_links and len(legacy_obj.various_links) > 10:
                for entry in legacy_obj.various_links.splitlines():
                    try:
                        validate_url(entry)
                        if len(entry) < 500:
                            rel = Relation(content_object=obj, url=entry)
                            log.debug('url (from various): %s' % rel.url)
                            rel.save()

                    except ValidationError, e:
                        print e

            """
            Label Mapping
            """
            legacy_items = LabelsReleases.objects.using('legacy').filter(release=legacy_obj)
            # r.tags.clear()
            for legacy_item in legacy_items:
                log.debug('mapping label')
                item, s = get_label_by_legacy_object(legacy_item.label)
                obj.label = item

            """
            User mapping
            """
            try:
                legacy_user = get_user_model().objects.using('legacy').get(id=legacy_obj.user_id)
                log.debug('mapping user')
                item, s = get_user_by_legacy_object(legacy_user)
                if item:
                    obj.creator = item
            except:
                pass

            """
            Tag Mapping
            """
            nts = NtagsReleases.objects.using('legacy').filter(release_id=legacy_obj.id)
            # r.tags.clear()
            for nt in nts:
                try:
                    t = Ntags.objects.using('legacy').get(id=nt.ntag_id)
                    log.debug('tag for object: %s' % t.name)
                    Tag.objects.add_tag(obj, u'"%s"' % t.name[:30])
                except Exception, e:
                    print e

            """
            Get image
            """
            try:
                img_path = os.path.join(LEGACY_STORAGE_ROOT, 'images', 'release', id_to_location(obj.legacy_id), 'original.jpg')
                log.debug('image path: %s' % img_path)
                if os.path.isfile(img_path):
                    img = get_file_from_path(img_path)
                    obj.main_image = img
                else:
                    log.debug('image does not exist at: %s' % img_path)

            except Exception, e:
                log.warning('unable to get image: %s - %s' % (img_path, e))

            obj.save()

        return obj, status


class MediaMigrator(Migrator):

    def __init__(self):
        log = logging.getLogger('util.migrator.__init__')


    def run(self, legacy_obj, force=False):

        from alibrary.models import Media, Relation

        status = 1

        log = logging.getLogger('util.migrator.run')
        log.info('migrate media: %s' % legacy_obj.name)

        obj, created = Media.objects.get_or_create(legacy_id=legacy_obj.id)

        if created:
            log.info('object created: %s' % obj.pk)
        else:
            log.info('object %s found by legacy_id: %s' % (obj.pk, obj.legacy_id))

        if created or force:
            """
            Mapping data
            1-to-1 fields
            """
            obj.name = legacy_obj.name
            obj.created = legacy_obj.created
            obj.updated = legacy_obj.updated
            obj.original_filename = legacy_obj.filename[0:250] if legacy_obj.filename else None
            #if legacy_obj.published:
            #    obj.publish_date = legacy_obj.published

            if legacy_obj.tracknumber:
                log.debug('tracknumber: %s' % legacy_obj.tracknumber)
                try:
                    obj.tracknumber = int(legacy_obj.tracknumber)
                except:
                    pass

            """
            Relation mapping
            """

            if legacy_obj.mb_trackid and legacy_obj.mb_trackid != 'nf':
                url = 'http://musicbrainz.org/recording/%s' % legacy_obj.mb_trackid
                log.debug('mb_trackid: %s' % url)
                rel = Relation(content_object=obj, url=url)
                rel.save()

            if legacy_obj.soundcloud_url and legacy_obj.soundcloud_url != 'nf':
                rel = Relation(content_object=obj, url=legacy_obj.soundcloud_url)
                log.debug('url: %s' % rel.url)
                rel.save()

            if legacy_obj.youtube_url and legacy_obj.youtube_url != 'nf':
                rel = Relation(content_object=obj, url=legacy_obj.youtube_url)
                log.debug('url: %s' % rel.url)
                rel.save()

            """
            Release Mapping
            """
            legacy_items = MediasReleases.objects.using('legacy').filter(media=legacy_obj)
            # r.tags.clear()
            for legacy_item in legacy_items:
                log.debug('mapping release')
                item, s = get_release_by_legacy_object(legacy_item.release)
                obj.release = item

            """
            Artist Mapping
            """
            legacy_items = ArtistsMedias.objects.using('legacy').filter(media=legacy_obj)
            # r.tags.clear()
            for legacy_item in legacy_items:
                log.debug('mapping artist')
                item, s = get_artist_by_legacy_object(legacy_item.artist)
                obj.artist = item

            """
            User mapping
            """
            try:
                legacy_user = get_user_model().objects.using('legacy').get(id=legacy_obj.user_id)
                log.debug('mapping user')
                item, s = get_user_by_legacy_object(legacy_user)
                if item:
                    obj.creator = item
            except:
                pass

            """
            Tag Mapping
            """
            nts = NtagsMedias.objects.using('legacy').filter(media_id=legacy_obj.id)
            for nt in nts:
                try:
                    t = Ntags.objects.using('legacy').get(id=nt.ntag_id)
                    log.debug('tag for object: %s' % t.name)
                    Tag.objects.add_tag(obj, u'"%s"' % t.name[:30])
                except Exception, e:
                    print e



            """
            License mapping
            """
            license_id = None
            if legacy_obj.license_id:
                license_id = legacy_obj.license_id
                log.debug('got license from media - license id: %s' % license_id)
            else:
                try:
                    license_id = MediasReleases.objects.using('legacy').filter(media=legacy_obj)[0].release.license_id
                    log.debug('got license from release - license id: %s' % license_id)
                except Exception, e:
                    log.warning('unable to find license: %s' % e)

            if license_id:
                from alibrary.models import License
                obj.license, c = License.objects.get_or_create(legacy_id=license_id)




            """
            migrate actual file
            """


            legacy_dir = os.path.join(LEGACY_STORAGE_ROOT, 'media', id_to_location(obj.legacy_id))

            log.debug('legacy dir: %s' % legacy_dir)
            log.debug('legacy dataformat: %s' % legacy_obj.dataformat)

            if legacy_obj.dataformat == 'flac' and os.path.isfile(os.path.join(legacy_dir, 'default.flac')):
                legacy_path = os.path.join(legacy_dir, 'default.flac')
                log.debug('got FLAC file: %s' % legacy_path)

            #elif legacy_obj.dataformat == 'wav' and os.path.isfile(os.path.join(legacy_dir, 'default.wav')):
            #    legacy_path = os.path.join(legacy_dir, 'default.wav')
            #    log.debug('got WAVE file: %s' % legacy_path)

            elif legacy_obj.dataformat == 'm4a' and os.path.isfile(os.path.join(legacy_dir, 'default.m4a')):
                legacy_path = os.path.join(legacy_dir, 'default.m4a')
                log.debug('got M4A file: %s' % legacy_path)

            elif legacy_obj.dataformat == 'mp4' and os.path.isfile(os.path.join(legacy_dir, 'default.mp4')):
                legacy_path = os.path.join(legacy_dir, 'default.mp4')
                log.debug('got MP4 file: %s' % legacy_path)

            #elif legacy_obj.dataformat == 'vorbis' and os.path.isfile(os.path.join(legacy_dir, 'default.vorbis')):
            #    legacy_path = os.path.join(legacy_dir, 'default.vorbis')
            #    log.debug('got OGG/Vorbis file: %s' % legacy_path)

            #elif legacy_obj.dataformat == 'ogg' and os.path.isfile(os.path.join(legacy_dir, 'default.ogg')):
            #    legacy_path = os.path.join(legacy_dir, 'default.ogg')
            #    log.debug('got OGG file: %s' % legacy_path)

            else:
                legacy_path = os.path.join(legacy_dir, 'default.mp3')
                log.debug('got MP3 file: %s' % legacy_path)


            """
            if legacy_obj.has_flac_default == 1 and os.path.isfile(os.path.join(legacy_dir, 'default.flac')):
                legacy_path = os.path.join(legacy_dir, 'default.flac')
                log.debug('got FLAC file: %s' % legacy_path)
            else:
                legacy_path = os.path.join(legacy_dir, 'default.mp3')
                log.debug('got MP3 file: %s' % legacy_path)
            """


            log.debug('legacy path: %s' % legacy_path)

            if os.path.isfile(legacy_path):
                obj.master = get_file_from_path(legacy_path)

            else:
                log.warning('file does not exist: %s' % legacy_path)


            try:
                pass
            except Exception, e:
                print e




            obj.save()

        return obj, status


class ArtistMigrator(Migrator):

    def __init__(self):
        log = logging.getLogger('util.migrator.__init__')


    def run(self, legacy_obj, force=False):

        from alibrary.models import Artist, Relation

        status = 1

        log = logging.getLogger('util.migrator.run')
        log.info('migrate artist: %s' % legacy_obj.name)

        obj, created = Artist.objects.get_or_create(legacy_id=legacy_obj.id)

        if created:
            log.info('object created: %s' % obj.pk)
        else:
            log.info('object found by legacy_id: %s' % obj.pk)

        if created or force:
            """
            Mapping data
            1-to-1 fields
            """
            obj.name = legacy_obj.name
            obj.created = legacy_obj.created
            obj.updated = legacy_obj.updated
            #obj.published = legacy_obj.published

            if legacy_obj.profile:
                obj.biography = legacy_obj.profile

            if legacy_obj.artisttype:
                obj.type = legacy_obj.artisttype

            if legacy_obj.realname:
                obj.real_name = legacy_obj.realname

            if legacy_obj.country:
                log.debug('country: %s' % legacy_obj.country)
                country = None
                if len(legacy_obj.country) == 2:
                    try:
                        country = Country.objects.get(iso2_code=legacy_obj.country)
                    except Exception, e:
                        pass

                else:
                    try:
                        country = Country.objects.get(printable_name=legacy_obj.country)
                    except Exception, e:
                        pass

                if country:
                    log.debug('got country: %s' % country.name)
                    obj.country = country

            if legacy_obj.aliases:
                log.debug('aliases: %s' % legacy_obj.aliases)
                for alias in legacy_obj.aliases.split(','):
                    log.debug('alias: %s' % alias)
                    try:
                        a, c = Artist.objects.get_or_create(name=alias.rstrip(' ').lstrip(' '))
                        obj.aliases.add(a)
                    except:
                        try:
                            a = Artist.objects.filter(name=alias.rstrip(' ').lstrip(' '))[0]
                            obj.aliases.add(a)
                        except:
                            pass

            """
            Relation mapping
            """
            if legacy_obj.discogs_artistid and legacy_obj.discogs_artistid != 'nf':
                url = 'http://www.discogs.com/artist/%s' % legacy_obj.discogs_artistid
                log.debug('discogs_url: %s' % url)
                rel = Relation(content_object=obj, url=url)
                rel.save()

            if legacy_obj.mb_artistid and legacy_obj.mb_artistid != 'nf':
                url = 'http://musicbrainz.org/artist/%s' % legacy_obj.mb_artistid
                log.debug('mb_artistid: %s' % url)
                rel = Relation(content_object=obj, url=url)
                rel.save()

            if legacy_obj.myspace_url and legacy_obj.myspace_url != 'nf':
                rel = Relation(content_object=obj, url=legacy_obj.myspace_url)
                log.debug('url: %s' % rel.url)
                rel.save()

            if legacy_obj.wikipedia_url and legacy_obj.wikipedia_url != 'nf':
                rel = Relation(content_object=obj, url=legacy_obj.wikipedia_url)
                log.debug('url: %s' % rel.url)
                rel.save()

            if legacy_obj.facebook_url and legacy_obj.facebook_url != 'nf':
                rel = Relation(content_object=obj, url=legacy_obj.facebook_url)
                log.debug('url: %s' % rel.url)
                rel.save()

            if legacy_obj.lastfm_url and legacy_obj.lastfm_url != 'nf':
                rel = Relation(content_object=obj, url=legacy_obj.lastfm_url)
                log.debug('url: %s' % rel.url)
                rel.save()

            if legacy_obj.soundcloud_url and legacy_obj.soundcloud_url != 'nf':
                rel = Relation(content_object=obj, url=legacy_obj.soundcloud_url)
                log.debug('url: %s' % rel.url)
                rel.save()

            if legacy_obj.website and legacy_obj.website != 'nf':
                rel = Relation(content_object=obj, url=legacy_obj.website, service='official')
                log.debug('url: %s' % rel.url)
                rel.save()

            if legacy_obj.various_links and len(legacy_obj.various_links) > 10:
                for entry in legacy_obj.various_links.splitlines():
                    try:
                        validate_url(entry)
                        if len(entry) < 500:
                            rel = Relation(content_object=obj, url=entry)
                            log.debug('url (from various): %s' % rel.url)
                            rel.save()

                    except ValidationError, e:
                        print e

            """
            User mapping
            """
            try:
                legacy_user = get_user_model().objects.using('legacy').get(id=legacy_obj.user_id)
                log.debug('mapping user')
                item, s = get_user_by_legacy_object(legacy_user)
                if item:
                    obj.creator = item
            except:
                pass

            """
            Tag Mapping
            """
            nts = NtagsArtists.objects.using('legacy').filter(artist_id=legacy_obj.id)
            # r.tags.clear()
            for nt in nts:
                try:
                    t = Ntags.objects.using('legacy').get(id=nt.ntag_id)
                    log.debug('tag for object: %s' % t.name)
                    Tag.objects.add_tag(obj, u'"%s"' % t.name[:30])
                except Exception, e:
                    print e

            """
            Get image
            """
            try:
                img_path = os.path.join(LEGACY_STORAGE_ROOT, 'images', 'artist', id_to_location(obj.legacy_id), 'original.jpg')
                log.debug('image path: %s' % img_path)
                if os.path.isfile(img_path):
                    img = get_file_from_path(img_path)
                    obj.main_image = img
                else:
                    log.debug('image does not exist at: %s' % img_path)

            except Exception, e:
                log.warning('unable to get image: %s - %s' % (img_path, e))

            obj.save()

        return obj, status


class LabelMigrator(Migrator):

    def __init__(self):
        log = logging.getLogger('util.migrator.__init__')


    def run(self, legacy_obj, force=False):

        from alibrary.models import Label, Relation, Distributor, DistributorLabel

        status = 1

        log = logging.getLogger('util.migrator.run')
        log.info('migrate release: %s' % legacy_obj.name)

        obj, created = Label.objects.get_or_create(legacy_id=legacy_obj.id)

        if created:
            log.info('object created: %s' % obj.pk)
        else:
            log.info('object found by legacy_id: %s' % obj.pk)

        if created or force:
            """
            Mapping data
            1-to-1 fields
            """
            obj.name = legacy_obj.name
            obj.created = legacy_obj.created
            obj.updated = legacy_obj.updated

            #if legacy_obj.published:
            #    obj.published = legacy_obj.published

            if legacy_obj.label_type:
                obj.type = legacy_obj.label_type

            if legacy_obj.label_code:
                log.debug('label_code: %s' % legacy_obj.label_code)
                obj.labelcode = legacy_obj.label_code[:200]

            if legacy_obj.profile:
                if legacy_obj.notes:
                    obj.description = "%s\n\n%s" % (legacy_obj.profile, legacy_obj.notes)
                else:
                    obj.description = legacy_obj.profile

            if legacy_obj.address:
                obj.address = legacy_obj.address

            if legacy_obj.contact:
                log.debug('contact: %s' % legacy_obj.contact)
                if email_re.match(legacy_obj.contact):
                    obj.email = legacy_obj.contact

            if legacy_obj.country:
                log.debug('country: %s' % legacy_obj.country)
                country = None
                if len(legacy_obj.country) == 2:
                    try:
                        country = Country.objects.get(iso2_code=legacy_obj.country)
                    except Exception, e:
                        pass

                else:
                    try:
                        country = Country.objects.get(printable_name=legacy_obj.country)
                    except Exception, e:
                        pass

                if country:
                    log.debug('got country: %s' % country.name)
                    obj.country = country

            if legacy_obj.distributor:
                log.debug('distributor: %s' % legacy_obj.distributor)
                d, c = Distributor.objects.get_or_create(name=legacy_obj.distributor)
                dl = DistributorLabel(distributor=d, label=obj)
                dl.save()

            """
            Relation mapping
            """
            if legacy_obj.discogs_labelid and legacy_obj.discogs_labelid != 'nf':
                url = 'http://www.discogs.com/label/%s' % legacy_obj.discogs_labelid
                log.debug('discogs_url: %s' % url)
                rel = Relation(content_object=obj, url=url)
                rel.save()

            if legacy_obj.mb_labelid and legacy_obj.mb_labelid != 'nf':
                url = 'http://musicbrainz.org/label/%s' % legacy_obj.mb_labelid
                log.debug('mb_labelid: %s' % url)
                rel = Relation(content_object=obj, url=url)
                rel.save()

            if legacy_obj.facebook_url and legacy_obj.facebook_url != 'nf':
                rel = Relation(content_object=obj, url=legacy_obj.facebook_url)
                log.debug('url: %s' % rel.url)
                rel.save()

            if legacy_obj.wikipedia_url and legacy_obj.wikipedia_url != 'nf':
                rel = Relation(content_object=obj, url=legacy_obj.wikipedia_url)
                log.debug('url: %s' % rel.url)
                rel.save()

            if legacy_obj.soundcloud_url and legacy_obj.soundcloud_url != 'nf':
                rel = Relation(content_object=obj, url=legacy_obj.soundcloud_url)
                log.debug('url: %s' % rel.url)
                rel.save()

            if legacy_obj.lastfm_url and legacy_obj.lastfm_url != 'nf':
                rel = Relation(content_object=obj, url=legacy_obj.lastfm_url)
                log.debug('url: %s' % rel.url)
                rel.save()

            if legacy_obj.website and legacy_obj.website != 'nf':
                rel = Relation(content_object=obj, url=legacy_obj.website, service='official')
                log.debug('url: %s' % rel.url)
                rel.save()

            if legacy_obj.various_links and len(legacy_obj.various_links) > 10:
                for entry in legacy_obj.various_links.splitlines():

                    try:
                        validate_url(entry)
                        if len(entry) < 500:
                            rel = Relation(content_object=obj, url=entry)
                            log.debug('url (from various): %s' % rel.url)
                            rel.save()

                    except ValidationError, e:
                        print e

            """
            User mapping
            """
            try:
                legacy_user = get_user_model().objects.using('legacy').get(id=legacy_obj.user_id)
                log.debug('mapping user')
                item, s = get_user_by_legacy_object(legacy_user)
                if item:
                    obj.creator = item
            except:
                pass

            """
            Tag Mapping
            """
            nts = NtagsLabels.objects.using('legacy').filter(label_id=legacy_obj.id)
            # r.tags.clear()
            for nt in nts:
                try:
                    t = Ntags.objects.using('legacy').get(id=nt.ntag_id)
                    log.debug('tag for object: %s' % t.name)
                    Tag.objects.add_tag(obj, u'"%s"' % t.name[:30])
                except Exception, e:
                    print e

            """
            Get image
            """
            try:
                img_path = os.path.join(LEGACY_STORAGE_ROOT, 'images', 'label', id_to_location(obj.legacy_id), 'original.jpg')
                log.debug('image path: %s' % img_path)
                if os.path.isfile(img_path):
                    img = get_file_from_path(img_path)
                    obj.main_image = img
                else:
                    log.debug('image does not exist at: %s' % img_path)

            except Exception, e:
                log.warning('unable to get image: %s - %s' % (img_path, e))

            obj.save()

        return obj, status


class LicenseMigrator(Migrator):

    def __init__(self):
        log = logging.getLogger('util.migrator.__init__')


    def run(self, legacy_obj, force=False):

        from alibrary.models import License

        status = 1

        log = logging.getLogger('util.migrator.run')
        log.info('migrate license: %s' % legacy_obj.id)

        obj, created = License.objects.get_or_create(legacy_id=legacy_obj.id)

        if created:
            log.info('object created: %s' % obj.pk)
        else:
            log.info('object found by legacy_id: %s' % obj.pk)

        if created or force:
            """
            Mapping data
            1-to-1 fields
            """
            obj.name = legacy_obj.key
            obj.key = legacy_obj.key
            obj.slug = legacy_obj.key.replace('_', '-')


            if legacy_obj.restricted == 1:
                obj.restricted = True
            else:
                obj.restricted = False



            obj.save()

        return obj, status


class UserMigrator(Migrator):
    def __init__(self):
        log = logging.getLogger('util.migrator.__init__')


    def run(self, legacy_obj, force=False):

        from profiles.models import Profile
        #from obp_legacy.models_legacy import *

        status = 1

        log = logging.getLogger('util.migrator.run')
        log.info('migrate user: %s' % legacy_obj.username)

        try:
            obj = Profile.objects.get(legacy_id=legacy_obj.id).user
        except:
            obj = None

        return obj, status


class LegacyUserMigrator(Migrator):
    def __init__(self):
        log = logging.getLogger('util.migrator.__init__')


    def run(self, legacy_obj, force=False):

        force = True

        from django.contrib.auth.models import Group
        from django.contrib.auth import get_user_model
        from profiles.models import Profile, Link, Service, ServiceType, Expertise, Community
        from obp_legacy.models_legacy import *
        from phonenumber_field.validators import validate_international_phonenumber

        status = 1

        log = logging.getLogger('util.migrator.run')
        log.info('migrate user: %s' % legacy_obj.username)

        user, created = get_user_model().objects.get_or_create(username=legacy_obj.username)
        obj = user.profile

        if created or force:

            user.email = legacy_obj.email


            # add user to 'member' group
            mg, c = Group.objects.get_or_create(name='Member')
            user.groups.add(mg)



            #obj.legacy_id = legacy_obj.id
            obj.legacy_legacy_id = legacy_obj.ident

            """
            Try to get legacy id (not legacy_legacy_id)
            """
            obj.legacy_id = get_user_model().objects.using('legacy').get(legacy_id=legacy_obj.ident).id

            """
            user.last_login = legacy_obj.created
            user.date_joined = legacy_obj.updated
            """
            if legacy_obj.name:
                name = legacy_obj.name.split(' ')

                if len(name) == 1:
                    user.last_name = name[0][:29]

                if len(name) == 2:
                    user.first_name = name[0][:29]
                    user.last_name = name[1][:29]

                if len(name) > 2:
                    user.first_name = name[0][:29]
                    user.last_name = ' '.join(name[1:])[:29]

                print 'name:       %s' % name
                print 'first_name: %s' % user.first_name
                print 'last_name:  %s' % user.last_name



            print 'last_action: %s' % legacy_obj.last_action
            print 'join_date: %s' % legacy_obj.join_date

            if legacy_obj.last_action and legacy_obj.last_action > 0:
                user.last_login = datetime.datetime.fromtimestamp(int(legacy_obj.last_action)).strftime('%Y-%m-%d %H:%M:%S')
            else:
                #user.last_login = datetime.datetime.strftime('2008-01-01 12:00:00')
                pass

            if legacy_obj.join_date and legacy_obj.join_date > 0:
                user.date_joined = datetime.datetime.fromtimestamp(int(legacy_obj.join_date)).strftime('%Y-%m-%d %H:%M:%S')


            user.save()

            """
            try to get a profile image
            """
            if legacy_obj.icon and not legacy_obj.icon == -1:
                print 'seems to have a profile icon: %s' % legacy_obj.icon
                li = ElggIcons.objects.using('legacy_legacy').filter(ident=legacy_obj.icon)
                if li.count() > 0:
                    li = li[0]
                    print li.filename

                    try:
                        img_path = os.path.join(LEGACY_STORAGE_ROOT, 'icons', legacy_obj.username[0:1], legacy_obj.username, li.filename)
                        log.debug('image path: %s' % img_path)
                        if os.path.isfile(img_path):
                            obj.image = get_file_from_path(img_path)
                        else:
                            log.debug('image does not exist at: %s' % img_path)

                    except Exception, e:
                        log.warning('unable to get image: %s - %s' % (img_path, e))


            """
            try to get communities
            """
            try:
                group_ids = ElggFriends.objects.using('legacy_legacy').values_list('friend', flat=True).filter(owner=legacy_obj.ident)
                groups = ElggUsers.objects.using('legacy_legacy').values_list('name', flat=True).filter(ident__in=group_ids, user_type='community')
                communities = Community.objects.filter(name__in=[name for name in groups.all()])
                for community in communities:
                    community.members.add(user)
            except:
                pass

            """
            try to get 'friends'
            """
            try:
                group_ids = ElggFriends.objects.using('legacy_legacy').values_list('friend', flat=True).filter(owner=legacy_obj.ident)
                friends = ElggUsers.objects.using('legacy_legacy').values_list('username', flat=True).filter(ident__in=group_ids, user_type='person')
                users = get_user_model().objects.filter(username__in=[username for username in friends.all()])

                print users
                from actstream.actions import follow
                for tu in users:
                    follow(user, tu)

                #communities = Community.objects.filter(name__in=[name for name in groups.all()])
                #for community in communities:
                #    community.members.add(user)
            except Exception, e:
                print e
                pass




            #obj, created = Profile.objects.get_or_create(legacy_id=legacy_obj.id, user=user)

            """
            Gathering profile data
            """
            p_data = ElggProfileData.objects.using('legacy_legacy').filter(owner=legacy_obj.ident)
            """"""
            print '//////////////////////////////////////////////'
            print 'legacy user data'
            print
            for item in p_data:
                """"""
                print 'access: %s' % item.access
                print 'name: %s' % item.name
                print 'value: %s' % item.value
                print

                """
                Mapping profile data
                """
                if item.name == 'interests':
                    # mapped to tags
                    tags = item.value.split(',')
                    for tag in tags:
                        tag = tag.rstrip(' ').lstrip(' ')
                        if len(tag) > 2:
                            try:
                                Tag.objects.add_tag(obj, u'"%s"' % tag[:30])
                            except Exception, e:
                                print e

                if item.name == 'formats':
                    # mapped to tags
                    tags = item.value.split(',')
                    for tag in tags:
                        tag = tag.rstrip(' ').lstrip(' ')
                        if len(tag) > 2:
                            try:
                                Tag.objects.add_tag(obj, u'"%s"' % tag[:30])
                            except Exception, e:
                                print e

                """
                address/contact related
                """
                if item.name == 'emailaddress':
                    obj.user.email = item.value

                if item.name == 'homestreetaddress':
                    obj.address1 = item.value

                if item.name == 'homepostcode':
                    obj.zip = item.value

                if item.name == 'hometown':
                    obj.city = item.value

                if item.name == 'homephone':
                    try:
                        validate_international_phonenumber(item.value)
                        if not obj.phone:
                            obj.phone = item.value

                    except ValidationError:
                        pass

                if item.name == 'workphone':
                    try:
                        validate_international_phonenumber(item.value)
                        if not obj.phone:
                            obj.phone = item.value

                    except ValidationError:
                        pass

                if item.name == 'mobphone':
                    try:
                        validate_international_phonenumber(item.value)
                        obj.phone = item.value

                    except ValidationError:
                        pass

                if item.name == 'homecountry':
                    country = None
                    if len(item.value) == 2:
                        try:
                            country = Country.objects.get(iso2_code=item.value)
                        except Exception, e:
                            pass

                    else:
                        try:
                            country = Country.objects.get(printable_name=item.value)
                        except Exception, e:
                            pass

                    if country:
                        obj.country = country


                """
                description / biography & co
                """
                if item.name == 'artistname':
                    obj.pseudonym = item.value[0:240]

                if item.name == 'minibio':
                    obj.description = item.value[0:240]

                if item.name == 'biography':
                    obj.biography = item.value

                if item.name == 'ibanprivate':
                    obj.iban = item.value

                if item.name == 'gender':
                    if item.value == 'male':
                        obj.gender = 0
                    elif item.value == 'female':
                        obj.gender = 1
                    else:
                        obj.gender = 2

                if item.name == 'birth_date':
                    try:
                        valid_date = time.strptime('%s' % item.value, '%Y-%m-%d')
                        obj.birth_date = item.value
                    except Exception, e:
                        print e


                """
                links
                """
                if item.name == 'workweb':
                    url = item.value
                    if not url[0:7] == 'http://':
                        url = 'http://' + url
                    link, c = Link.objects.get_or_create(profile=obj, url=url)
                    link.title = 'Work website'
                    link.save()

                if item.name in ['personalweb', 'personalweb1', 'personalweb2', 'personalweb3', 'personalweb4', 'personalweb5']:
                    url = item.value
                    if not url[0:7] == 'http://':
                        url = 'http://' + url
                    link, c = Link.objects.get_or_create(profile=obj, url=url)
                    link.title = 'Personal website'
                    link.save()

                """
                services
                """
                if item.name in ['msn', 'icq', 'skype', 'aim', 'twitter',]:
                    service_type, c = ServiceType.objects.get_or_create(title=item.name.capitalize())
                    service, c = Service.objects.get_or_create(service=service_type,
                                                               profile=obj,
                                                               username=item.value.rstrip(' ').lstrip(' '))


                """
                skills & professions
                """
                if item.name in ['profession', 'skills___']:
                    print 'parsing %s' % item.name

                    expertises = item.value.split(',')
                    for expertise in expertises:
                        expertise = expertise.rstrip(' ').lstrip(' ')
                        db_expertise, c = Expertise.objects.get_or_create(name=u'%s' % expertise.title())
                        obj.expertise.add(db_expertise)




            if created:
                log.info('object created: %s' % obj.pk)
            else:
                log.info('object found by legacy_id: %s' % obj.pk)

            if created:
                """
                Mapping data
                1-to-1 fields
                """

            obj.save()

        return obj, status


class CommunityMigrator(Migrator):
    def __init__(self):
        log = logging.getLogger('util.migrator.__init__')


    def run(self, legacy_obj):

        from profiles.models import Community
        from obp_legacy.models_legacy import *

        status = 1

        log = logging.getLogger('util.migrator.run')
        log.info('migrate user: %s' % legacy_obj.username)

        obj, created = Community.objects.get_or_create(name=legacy_obj.name)

        """
        Get image
        """
        try:
            icon = int(legacy_obj.icon)
            if icon > 0:
                img_url = 'https://www.openbroadcast.org/_icon/user/%s/h/300/w/300/302' % icon
                log.debug('download image: %s' % img_url)
            #obj.image = img
        except Exception, e:
            print e
            pass



        #obj, created = Profile.objects.get_or_create(legacy_id=legacy_obj.id, user=user)

        """
        Gathering profile data
        """
        p_data = ElggProfileData.objects.using('legacy_legacy').filter(owner=legacy_obj.ident)
        """"""
        for item in p_data:
            print 'access: %s' % item.access
            print 'name: %s' % item.name
            print 'value: %s' % item.value


            """
            mapping data profile
            """
            if item.name == 'interests':
                # interests are converted to tags
                tags = item.value.split(',')
                for tag in tags:
                    tag = tag.rstrip(' ').lstrip(' ')
                    if len(tag) > 2:
                        try:
                            Tag.objects.add_tag(obj, u'"%s"' % tag[:30])
                        except Exception, e:
                            print e


            """
            contact related
            """
            if item.name == 'homestreetaddress':
                obj.address1 = item.value

            if item.name == 'homepostcode':
                obj.zip = item.value

            if item.name == 'hometown':
                obj.city = item.value

            if item.name == 'homephone':
                obj.phone = item.value

            if item.name == 'mobphone':
                obj.phone = item.value

            if item.name == 'emailaddress':
                # assigned to user, not profile
                obj.email = item.value

            if item.name == 'homecountry':
                # tries to find country by iso code or full name (english only)
                country = None
                if len(item.value) == 2:
                    try:
                        country = Country.objects.get(iso2_code=item.value)
                    except Exception, e:
                        pass

                else:
                    try:
                        country = Country.objects.get(printable_name=item.value)
                    except Exception, e:
                        pass

                if country:
                    #log.debug('got country: %s' % country.name)
                    obj.country = country



            if item.name == 'minibio':
                obj.description = item.value



        #obj.legacy_id = legacy_obj.id
        obj.legacy_legacy_id = legacy_obj.ident

        if created:
            log.info('object created: %s' % obj.pk)
        else:
            log.info('object found by legacy_id: %s' % obj.pk)

        if created:
            """
            Mapping data
            1-to-1 fields
            """

        obj.save()

        return obj, status


class PlaylistMigrator(Migrator):
    def __init__(self):
        log = logging.getLogger('util.migrator.__init__')


    def run(self, legacy_obj, force):

        from alibrary.models import Playlist, PlaylistItemPlaylist
        from obp_legacy.models_legacy import *

        status = 1

        log = logging.getLogger('util.migrator.run')
        log.info('playlist: %s' % legacy_obj.title)

        obj, created = Playlist.objects.get_or_create(legacy_id=legacy_obj.ident)

        if created:
            log.info('object created: %s' % obj.pk)
        else:
            log.info('object found by legacy_id: %s' % obj.pk)


        if created or force:
            """
            Mapping data
            """
            obj.name = legacy_obj.title


            """
            legacy status
            1: work in progress
            2: ready to schedule
            3: scheduled (not possible to go back)
            4: un-scheduled ?
            """

            if legacy_obj.status == 1:
                obj.status = 2
            if legacy_obj.status == 2:
                obj.status = 1
            if legacy_obj.status == 3:
                obj.status = 3
            if legacy_obj.status == 4:
                obj.status = 4

            """
            Type mapping
            """
            if legacy_obj.status in (2, 3, 4):
                obj.type = 'broadcast'
            if legacy_obj.status in (0, 1):
                # maybe exclude '0'
                obj.type = 'playlist'

            """
            Tag Mapping
            """
            nts = ElggTags.objects.using('legacy_legacy').filter(ref=legacy_obj.ident)
            for nt in nts:
                try:
                    log.debug('tag for object: %s' % nt.tag)
                    Tag.objects.add_tag(obj, u'"%s"' % nt.tag[:30])
                except Exception, e:
                    print e

            if legacy_obj.intro:
                print legacy_obj.intro
                obj.description = legacy_obj.intro

            # date mappings
            if legacy_obj.posted:
                obj.created = datetime.datetime.fromtimestamp(int(legacy_obj.posted)).strftime('%Y-%m-%d %H:%M:%S')

            if legacy_obj.lastupdate:
                obj.updated = datetime.datetime.fromtimestamp(int(legacy_obj.lastupdate)).strftime('%Y-%m-%d %H:%M:%S')

            # TODO: status mapping
            if legacy_obj.status:
                print 'status id: %s' % legacy_obj.status

            """
            User mapping
            """
            try:
                legacy_user = get_user_model().objects.using('legacy').get(legacy_id=legacy_obj.owner)
                log.debug('mapping user')
                item, s = get_user_by_legacy_object(legacy_user)
                if item:
                    obj.user = item
            except Exception, e:
                print e
                pass

            """
            Getting this f**ing hell stupd content-container thing...
            """
            cts = ElggCmContainer.objects.using('legacy_legacy').filter(x_ident=legacy_obj.ident, container_type="Playlist")

            if cts.count() > 0:
                container = cts[0]
            else:
                container = None

            if container and container.sub_type <= 4:

                print '** description (stripped) *************************************'
                print html2text(container.body)
                print
                obj.description = html2text(container.body.replace('&nbsp;', ''))

                print 'target_duration: %s' % container.target_duration
                """
                target duration, calculation
                """
                print 'calculated:      %s' % (int(container.target_duration) * 15 * 60 * 1000)

                print 'duration:        %s' % container.duration
                print 'sub_type:        %s' % container.sub_type
                print 'best_broadcast_segment: %s' % container.best_broadcast_segment
                print 'rotation_include: %s' % container.rotation_include

                obj.target_duration = (int(container.target_duration) * 15 * 60)

                """
                mapping of legacy dayparts.
                structure:
                  [1,1], [3,5], etc.
                  first element:
                    indicates the day, 1-indexed, so 1 dor monday, 7 for sunday
                  second element:
                    indicates the slot, 1-indexed.

                """
                try:
                    from alibrary.models.basemodels import Daypart
                    daypart_ids = []
                    bcs = json.loads(container.best_broadcast_segment)
                    for bc in bcs:
                        dp_offset = int(bc[0]) * 7 - 6
                        if bc[1] < 7:
                            dp_pk = bc[1] + dp_offset
                        else:
                            dp_pk = dp_offset
                        daypart_ids.append(dp_pk)

                    obj.dayparts = Daypart.objects.filter(pk__in=daypart_ids)
                except Exception, e:
                    print 'unable to sassign daypart: %s' % e




                PlaylistItemPlaylist.objects.filter(playlist=obj).delete()
                """"""
                legacy_media = json.loads(container.content_list)
                position = 0
                for lm in legacy_media:
                    print lm
                    if 'source' in lm and lm['source'] == 'ml' and 'ident' in lm:
                        tm = Medias.objects.using('legacy').get(id=int(lm['ident']))
                        print tm.name
                        print 'pos: %s' % position

                        media, s = get_media_by_legacy_object(tm)
                        print media.pk

                        #pi = PlaylistItem()

                        # map timing
                        timing = {
                            'fade_in': lm['fade_in'],
                            'fade_out': lm['fade_out'],
                            'cue_in': lm['offset_in'],
                            'cue_out': lm['offset_out'],
                        }

                        obj.add_items_by_ids(ids=[media.pk,], ct='media', timing=timing)

                        position += 1

            obj.save()

        return obj, status


def get_release_by_legacy_object(legacy_obj, force=False):
    migrator = ReleaseMigrator()
    obj, status = migrator.run(legacy_obj, force)

    return obj, status


def get_media_by_legacy_object(legacy_obj, force=False):
    migrator = MediaMigrator()
    obj, status = migrator.run(legacy_obj, force)

    return obj, status


def get_artist_by_legacy_object(legacy_obj, force=False):
    migrator = ArtistMigrator()
    obj, status = migrator.run(legacy_obj, force)

    return obj, status


def get_label_by_legacy_object(legacy_obj, force=False):
    migrator = LabelMigrator()
    obj, status = migrator.run(legacy_obj, force)

    return obj, status


def get_user_by_legacy_object(legacy_obj, force=False):
    migrator = UserMigrator()
    obj, status = migrator.run(legacy_obj, force)

    return obj, status


def get_playlist_by_legacy_object(legacy_obj, force=False):
    migrator = PlaylistMigrator()
    obj, status = migrator.run(legacy_obj, force)

    return obj, status


def get_license_by_legacy_object(legacy_obj, force=False):
    migrator = LicenseMigrator()
    obj, status = migrator.run(legacy_obj, force)

    return obj, status


"""
Double legacy shortcuts
"""


def get_user_by_legacy_legacy_object(legacy_obj, force=False):
    migrator = LegacyUserMigrator()
    obj, status = migrator.run(legacy_obj, force)

    return obj, status


def get_community_by_legacy_legacy_object(legacy_obj):
    migrator = CommunityMigrator()
    obj, status = migrator.run(legacy_obj)

    return obj, status


"""
helper
"""


def id_to_location(id):
    l = "%012d" % id
    return '%d/%d/%d' % (int(l[0:4]), int(l[4:8]), int(l[8:12]))





