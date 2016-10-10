# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import glob
import logging
import os
import uuid
from datetime import datetime, date, timedelta
from zipfile import ZipFile

import arating
import requests
import reversion
import tagging
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext as _
from django_date_extensions.fields import ApproximateDateField
from django_extensions.db.fields import AutoSlugField
from l10n.models import Country
from lib.fields import extra
from tagging.registry import register as tagging_register

from alibrary import settings as alibrary_settings
from ..models import Relation, License, MigrationMixin, Profession
from ..util.slug import unique_slugify
from ..util.storage import get_dir_for_object, OverwriteStorage

logger = logging.getLogger(__name__)

MUSICBRAINZ_HOST = getattr(settings, 'MUSICBRAINZ_HOST', 'musicbrainz.org')

TEMP_DIR = getattr(settings, 'TEMP_DIR', None)
FORCE_CATALOGNUMBER = False
LOOKUP_PROVIDERS = (
    ('discogs', _('Discogs')),
    ('musicbrainz', _('Musicbrainz')),
)

class ReleaseManager(models.Manager):

    def active(self):
        now = datetime.now()
        return self.get_queryset().filter(
                Q(publish_date__isnull=True) |
                Q(publish_date__lte=now)
                )


def upload_cover_to(instance, filename):
    filename, extension = os.path.splitext(filename)
    return os.path.join(get_dir_for_object(instance), 'cover%s' % extension.lower())

class Release(MigrationMixin):
    
    # core fields
    name = models.CharField(max_length=200, db_index=True)
    slug = AutoSlugField(populate_from='name', editable=True, blank=True, overwrite=True)
    license = models.ForeignKey(License, blank=True, null=True, related_name='release_license')
    release_country = models.ForeignKey(Country, blank=True, null=True)

    #uuid = UUIDField(primary_key=False)
    #uuid = UUIDField()
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    main_image = models.ImageField(verbose_name=_('Cover'), upload_to=upload_cover_to, storage=OverwriteStorage(), null=True, blank=True)

    if FORCE_CATALOGNUMBER:
        catalognumber = models.CharField(max_length=50)
    else:
        catalognumber = models.CharField(max_length=50, blank=True, null=True)

    """
    releasedate stores the 'real' time, approx is for inputs
    lik 2012-12 etc.
    """
    releasedate = models.DateField(blank=True, null=True)
    releasedate_approx = ApproximateDateField(verbose_name="Releasedate", blank=True, null=True)
    pressings = models.PositiveIntegerField(default=0)
    TOTALTRACKS_CHOICES = ((x, x) for x in range(1, 301))
    totaltracks = models.IntegerField(verbose_name=_('Total Tracks'), blank=True, null=True, choices=TOTALTRACKS_CHOICES)
    asin = models.CharField(max_length=150, blank=True)
    RELEASESTATUS_CHOICES = (
        (None, _('Not set')),
        ('official', _('Official')),
        ('promo', _('Promo')),
        ('bootleg', _('Bootleg')),
        ('other', _('Other')),
    )
    
    releasestatus = models.CharField(max_length=60, blank=True, choices=RELEASESTATUS_CHOICES)
    excerpt = models.TextField(blank=True, null=True)
    description = extra.MarkdownTextField(blank=True, null=True)
    releasetype = models.CharField(verbose_name="Release type", max_length=24, blank=True, null=True, choices=alibrary_settings.RELEASETYPE_CHOICES)
    label = models.ForeignKey('alibrary.Label', blank=True, null=True, related_name='release_label', on_delete=models.SET_NULL)
    media = models.ManyToManyField('alibrary.Media', through='ReleaseMedia', blank=True, related_name="releases")

    owner = models.ForeignKey(User, blank=True, null=True, related_name="releases_owner", on_delete=models.SET_NULL)
    creator = models.ForeignKey(User, blank=True, null=True, related_name="releases_creator", on_delete=models.SET_NULL)
    last_editor = models.ForeignKey(User, blank=True, null=True, related_name="releases_last_editor", on_delete=models.SET_NULL)
    publisher = models.ForeignKey(User, blank=True, null=True, related_name="releases_publisher", on_delete=models.SET_NULL)

    barcode = models.CharField(max_length=32, blank=True, null=True)

    extra_artists = models.ManyToManyField('alibrary.Artist', through='ReleaseExtraartists', blank=True)
    album_artists = models.ManyToManyField('alibrary.Artist', through='ReleaseAlbumartists', related_name="release_albumartists", blank=True)

    relations = GenericRelation(Relation)
    d_tags = tagging.fields.TagField(max_length=1024, verbose_name="Tags", blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    objects = ReleaseManager()

    # meta
    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Release')
        verbose_name_plural = _('Releases')
        ordering = ('-created', )
        
        permissions = (
            ('view_release', 'View Release'),
            ('edit_release', 'Edit Release'),
            ('merge_release', 'Merge Releases'),
            ('admin_release', 'Edit Release (extended)'),
        )
    
    
    def __unicode__(self):
        return self.name
    
    @property
    def classname(self):
        return self.__class__.__name__
    
    def get_versions(self):
        try:
            return reversion.get_for_object(self)
        except:
            return None

    @property
    def publish_date(self):
        # compatibility hack TODO: refactor all dependencies
        return datetime.utcnow()

    def get_extra_artists(self):
        ea = []
        for artist in self.extra_artists.all():
            ea.append(artist.name)
        return ea
    
    def get_last_revision(self):
        try:
            last_version = reversion.get_unique_for_object(self)[0]
            return last_version.revision
        except:
            return None
        
    def get_last_editor(self):
        
        latest_revision = self.get_last_revision()
        if latest_revision:
            return latest_revision.user

        return None

    
    def is_active(self):
        now = date.today()
        try:
            if not self.releasedate:
                return True
            
            if self.releasedate <= now:
                return True
        
        except:
            pass

        return False

    @property
    def is_promotional(self):
        # TODO: refactor to license query
        if self.releasedate:
            if self.releasedate > datetime.now().date():
                return True

        if License.objects.filter(media_license__in=self.get_media(),
                                  is_promotional=True).distinct().exists():
            return True


        return False

    @property
    def is_new(self):
        if self.is_promotional:
            return False
        if self.releasedate and self.releasedate >= (datetime.now()-timedelta(days=14)).date():
            return True

        return False


    
    def get_lookup_providers(self):
        
        providers = []
        for key, name in LOOKUP_PROVIDERS:
            relations = self.relations.filter(service=key)
            relation = None
            if relations.count() == 1:
                relation = relations[0]
                
            providers.append({'key': key, 'name': name, 'relation': relation})

        return providers

    def get_absolute_url(self):
        return reverse('alibrary-release-detail', kwargs={
            'pk': self.pk,
            'slug': self.slug,
        })

    def get_edit_url(self):
        return reverse("alibrary-release-edit", args=(self.pk,))

    def get_admin_url(self):
        return reverse("admin:alibrary_release_change", args=(self.pk,))

    def get_api_url(self):
        return reverse('api_dispatch_detail', kwargs={  
            'api_name': 'v1',  
            'resource_name': 'library/release',
            'pk': self.pk  
        }) + ''

    def get_api_simple_url(self):
        return reverse('api_dispatch_detail', kwargs={
            'api_name': 'v1',
            'resource_name': 'library/simplerelease',
            'pk': self.pk
        }) + ''
    
    
    def get_media(self):
        from alibrary.models import Media
        return Media.objects.filter(release=self)
    
    def get_products(self):
        return self.releaseproduct.all()
    
    def get_media_indicator(self):
        
        media = self.get_media()
        indicator = []

        if self.totaltracks:
            for i in range(self.totaltracks):
                indicator.append(0)
        
            for m in media:
                try:
                    indicator[m.tracknumber -1 ] = 3
                except Exception, e:
                    pass

        else:
            for m in media:
                indicator.append(2)
        
        return indicator
            
            
    def get_license(self):        
        
        licenses = License.objects.filter(media_license__in=self.get_media()).distinct()
        if not licenses.exists():
            return {'name': _(u'Not Defined')}

        if licenses.count() > 1:
            license, created = License.objects.get_or_create(name="Multiple")
            return license

        if licenses.count() == 1:
            return licenses[0]


    """
    compose artist display as string
    """
    def get_artist_display(self):

        artist_str = ''
        artists = self.get_artists()
        if len(artists) > 1:
            try:
                for artist in artists:
                    if artist['join_phrase']:
                        artist_str += ' %s ' % artist['join_phrase']
                    artist_str += artist['artist'].name
            except:
                artist_str = artists[0]['artist'].name
        else:
            try:
                artist_str = artists[0]['artist'].name
            except:
                try:
                    artist_str = artists[0].name
                except:
                    artist_str = _('Unknown Artist')

        return artist_str


    def get_artists(self):

        artists = []
        if self.album_artists.count() > 0:
            for albumartist in self.release_albumartist_release.all():
                artists.append({'artist': albumartist.artist, 'join_phrase': albumartist.join_phrase})
            return artists
        

        medias = self.get_media()
        for media in medias:
            artists.append(media.artist)
        
        artists = list(set(artists))
        if len(artists) > 1:
            from alibrary.models import Artist
            a, c = Artist.objects.get_or_create(name="Various Artists")
            artists = [a]
            
        return artists

    def get_extra_artists(self):

        artists = []
        
        roles = ReleaseExtraartists.objects.filter(release=self.pk)
        
        for role in roles:
            try:
                role.artist.profession = role.profession.name
                artists.append(role.artist)
            except:
                pass
 
        return artists
    
    def get_downloads(self):
        return None

    
    def get_download_url(self, format, version):
        
        return '%sdownload/%s/%s/' % (self.get_absolute_url(), format, version)

    def get_cache_file_path(self, format, version):
        
        tmp_directory = TEMP_DIR
        file_name = '%s_%s_%s.%s' % (format, version, str(self.uuid), 'zip')
        tmp_path = '%s/%s' % (tmp_directory, file_name)
        
        return tmp_path
    
    
    def clear_cache_file(self):

        tmp_directory = TEMP_DIR
        pattern = '*%s.zip' % (str(self.uuid))
        versions = glob.glob('%s/%s' % (tmp_directory, pattern))

        try:
            for version in versions:
                os.remove(version)
  
        except Exception as e:
            pass

    def get_cache_file(self, format, version):

        cache_file_path = self.get_cache_file_path(format, version)
        
        if os.path.isfile(cache_file_path):
            logger.info('serving from cache: %s' % (cache_file_path))
            return cache_file_path
            
        else:
            return self.build_cache_file(format, version)

    def build_cache_file(self, format, version):
        
        cache_file_path = self.get_cache_file_path(format, version)
        
        logger.info('building cache for: %s' % (cache_file_path))

        try:
            os.remove(cache_file_path)
  
        except Exception, e:
            pass


        archive_file = ZipFile(cache_file_path, "w")
        
        """
        adding corresponding media files
        """
        for media in self.get_media():
            media_cache_file = media.inject_metadata(format, version)

            # filename for the file archive
            file_name = '%02d - %s - %s' % (media.tracknumber, media.artist.name, media.name)
            file_name = '%s.%s' % (file_name.encode('ascii', 'ignore'), format)

            archive_file.write(media_cache_file.path, file_name)

            
        return cache_file_path

    def get_extraimages(self):
        return None


    # OBSOLETE
    def complete_by_mb_id(self, mb_id):

        obj = self

        log = logging.getLogger('alibrary.release.complete_by_mb_id')
        log.info('complete release, r: %s | mb_id: %s' % (obj.name, mb_id))
        
        inc = ('artists', 'url-rels', 'aliases', 'tags', 'recording-rels', 'work-rels', 'work-level-rels', 'artist-credits')
        url = 'http://%s/ws/2/release/%s/?fmt=json&inc=%s' % (MUSICBRAINZ_HOST, mb_id, "+".join(inc))
        
        r = requests.get(url)
        result = r.json()

        
        return obj
    
    

    
    def save(self, *args, **kwargs):

        self.clear_cache_file()        
        unique_slugify(self, self.name)

        # convert approx date to real one
        ad = self.releasedate_approx
        try:
            ad_y = ad.year
            ad_m = ad.month
            ad_d = ad.day
            if ad_m == 0:
                ad_m = 1        
            if ad_d == 0:
                ad_d = 1
            
            rd = datetime.strptime('%s/%s/%s' % (ad_y, ad_m, ad_d), '%Y/%m/%d')
            self.releasedate = rd
        except:
            self.releasedate = None

        super(Release, self).save(*args, **kwargs)




@receiver(post_save, sender=Release)
def release_post_save(sender, instance, **kwargs):
    # TODO: hackish workaround - improve!
    # delete duplicate albumartists (can be caused by generic 'merge')
    qs = instance.release_albumartist_release.all()
    to_keep = []
    to_delete = []
    for aa in qs:
        t = (aa.join_phrase, aa.artist)
        if not t in to_keep:
            to_keep.append(t)
        else:
            to_delete.append(aa.pk)

    if to_delete:
        qs.filter(pk__in=to_delete).delete()


try:
    tagging_register(Release)
except Exception as e:
    print e
    pass


arating.enable_voting_on(Release)

class ReleaseExtraartists(models.Model):
    artist = models.ForeignKey('alibrary.Artist', related_name='release_extraartist_artist')
    release = models.ForeignKey('Release', related_name='release_extraartist_release')
    profession = models.ForeignKey(Profession, verbose_name='Role/Profession', related_name='release_extraartist_profession', blank=True, null=True)   
    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')

class ReleaseAlbumartists(models.Model):
    artist = models.ForeignKey('alibrary.Artist', related_name='release_albumartist_artist')
    release = models.ForeignKey('Release', related_name='release_albumartist_release')

    join_phrase = models.CharField(verbose_name="join phrase", max_length=12, default=None, choices=alibrary_settings.ARTIST_JOIN_PHRASE_CHOICES, blank=True, null=True)
    position = models.PositiveIntegerField(null=True, blank=True)
    
    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Albumartist')
        verbose_name_plural = _('Albumartists')
        ordering = ('position', )

    def __unicode__(self):
        return '{0} - {1} {2}'.format(self.release, self.join_phrase, self.artist)

@receiver(post_delete, sender=ReleaseAlbumartists)
def release_albumartists_post_delete(sender, instance, **kwargs):
    # clear caches
    from alibrary.models import Artist
    Artist.get_releases.invalidate(instance.artist)
    Artist.get_media.invalidate(instance.artist)


class ReleaseRelations(models.Model):
    relation = models.ForeignKey('Relation', related_name='release_relation_relation')
    release = models.ForeignKey('Release', related_name='release_relation_release')
    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Relation')
        verbose_name_plural = _('Relations')


class ReleaseMedia(models.Model):
    release = models.ForeignKey('Release')
    media = models.ForeignKey('alibrary.Media')
    position = models.PositiveIntegerField(null=True, blank=True)
    class Meta:
        app_label = 'alibrary'
