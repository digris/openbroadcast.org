# python
import datetime
from datetime import *
import glob
from zipfile import ZipFile

import requests


# django
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from settings import *

from alibrary import settings as alibrary_settings

# django-extensions (http://packages.python.org/django-extensions/)
from django_extensions.db.fields import UUIDField

# cms
from cms.models import CMSPlugin, Page

# filer
from filer.models.filemodels import *
from filer.models.foldermodels import *
from filer.models.audiomodels import *
from filer.models.imagemodels import *
from filer.fields.image import FilerImageField
from filer.fields.audio import FilerAudioField
from filer.fields.file import FilerFileField


from l10n.models import Country

from django_date_extensions.fields import ApproximateDateField

# modules
#from taggit.managers import TaggableManager
from django_countries import CountryField

import tagging
import reversion 

# settings
from settings import TEMP_DIR

# logging
import logging
logger = logging.getLogger(__name__)

from alibrary.util.signals import library_post_save
from alibrary.util.slug import unique_slugify
from alibrary.util.storage import get_dir_for_object, OverwriteStorage

import arating
    
################

from alibrary.models.basemodels import *
from alibrary.models.artistmodels import *
from alibrary.models.labelmodels import Label
from alibrary.models.mediamodels import Media




FORCE_CATALOGNUMBER = False

# shop
#from ashop.models import Hardwarerelease, Downloadrelease

from lib.fields import extra


LOOKUP_PROVIDERS = (
    ('discogs', _('Discogs')),
    ('musicbrainz', _('Musicbrainz')),
)



class ReleaseManager(models.Manager):


    def active(self):
        now = datetime.now()
        return self.get_query_set().filter(
                Q(publish_date__isnull=True) |
                Q(publish_date__lte=now)
                )



def upload_cover_to(instance, filename):
    filename, extension = os.path.splitext(filename)
    return os.path.join(get_dir_for_object(instance), 'cover%s' % extension.lower())


def filename_by_uuid(instance, filename, root='release'):
    filename, extension = os.path.splitext(filename)
    filename = instance.uuid.replace('-', '/')[5:] + extension
    return os.path.join(root, filename)


class Release(MigrationMixin):
    
    # core fields
    uuid = UUIDField(primary_key=False)
    name = models.CharField(max_length=200, db_index=True)
    slug = AutoSlugField(populate_from='name', editable=True, blank=True, overwrite=True)
    
    license = models.ForeignKey(License, blank=True, null=True, related_name='release_license')

    release_country = models.ForeignKey(Country, blank=True, null=True)
    
    uuid = UUIDField()
    
    #main_image = FilerImageField(null=True, blank=True, related_name="release_main_image", rel='')
    main_image = models.ImageField(verbose_name=_('Cover'), upload_to=upload_cover_to, storage=OverwriteStorage(), null=True, blank=True)
    cover_image = FilerImageField(null=True, blank=True, related_name="release_cover_image", rel='', help_text=_('Cover close-up. Used e.g. for embedding in digital files.'))
    
    
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
    

    pressings = models.PositiveIntegerField(max_length=12, default=0)

    TOTALTRACKS_CHOICES = ((x, x) for x in range(1, 101))
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
    
    # publish_date = models.DateTimeField(default=datetime.now, blank=True, null=True, help_text=_('If set this Release will not be published on the site before the given date.'))
    # publish_date = models.DateTimeField(blank=True, null=True, help_text=_('If set this Release will not be published on the site before the given date.'))
    @property
    def publish_date(self):
        # compatibility hack TODO: refactor all dependencies
        return datetime.utcnow()

    main_format = models.ForeignKey(Mediaformat, null=True, blank=True, on_delete=models.SET_NULL)
    
    # 
    excerpt = models.TextField(blank=True, null=True)
    description = extra.MarkdownTextField(blank=True, null=True)


    releasetype = models.CharField(verbose_name="Release type", max_length=24, blank=True, null=True, choices=alibrary_settings.RELEASETYPE_CHOICES)

    
    # relations
    label = models.ForeignKey(Label, blank=True, null=True, related_name='release_label', on_delete=models.SET_NULL)
    folder = models.ForeignKey(Folder, blank=True, null=True, related_name='release_folder', on_delete=models.SET_NULL)
    
    
    # reworking media relationship
    media = models.ManyToManyField('Media', through='ReleaseMedia', blank=True, null=True, related_name="releases")
    #media = SortedManyToManyField('Media', blank=True, null=True, related_name="releases")
    

    # user relations
    owner = models.ForeignKey(User, blank=True, null=True, related_name="releases_owner", on_delete=models.SET_NULL)
    creator = models.ForeignKey(User, blank=True, null=True, related_name="releases_creator", on_delete=models.SET_NULL)
    publisher = models.ForeignKey(User, blank=True, null=True, related_name="releases_publisher", on_delete=models.SET_NULL)

    # identifiers
    barcode = models.CharField(max_length=32, blank=True, null=True)

    # generic reverse relations
    # import_items = generic.GenericRelation('importer.ImportItem')

    # extra-artists
    extra_artists = models.ManyToManyField('Artist', through='ReleaseExtraartists', blank=True, null=True)
    def get_extra_artists(self):
        ea = []
        for artist in self.extra_artists.all():
            ea.push(artist.name)
        return ea
    
    # special relation to provide 'multi-names' for artists.
    album_artists = models.ManyToManyField('Artist', through='ReleaseAlbumartists', related_name="release_albumartists", blank=True, null=True)
    
    # relations a.k.a. links
    relations = generic.GenericRelation(Relation)
    
    # tagging (d_tags = "display tags")
    d_tags = tagging.fields.TagField(max_length=1024, verbose_name="Tags", blank=True, null=True)
    
    enable_comments = models.BooleanField(_('Enable Comments'), default=True)
    
    # manager
    objects = ReleaseManager()
    
    # auto-update
    created = models.DateField(auto_now_add=True, editable=False)
    updated = models.DateField(auto_now=True, editable=False)

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
        
    
    def get_last_revision(self):
        try:
            return reversion.get_unique_for_object(self)[0].revision
        except:
            return None
        
    def get_last_editor(self):
        
        latest_revision = self.get_last_revision()
        
        if latest_revision:
            return latest_revision.user
        
        else:
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
        #if self.releasedate and self.publish_date:
        #    if self.releasedate > self.publish_date.date() and self.releasedate > datetime.now().date():
        #        return True

        if License.objects.filter(media_license__in=self.get_media(),
                                  is_promotional=True).distinct().exists():
            return True


        return False

    @property
    def is_new(self):
        if self.releasedate and self.releasedate > (datetime.now()-timedelta(days=7)).date():
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
    

    @models.permalink
    def get_absolute_url(self):
        return ('alibrary-release-detail', [self.slug])

    @models.permalink
    def get_edit_url(self):
        return ('alibrary-release-edit', [self.pk])
    
    def get_admin_url(self):
        from lib.util.get_admin_url import change_url
        return change_url(self)
    
    

    
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
        return Media.objects.filter(release=self).order_by('tracknumber', 'name').select_related()
    
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
        
        license = None
        
        if licenses.count() == 1:
            license = licenses[0]
        if licenses.count() > 1:
            license, created = License.objects.get_or_create(name="Multiple")
            
        return license


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
                artist_str = artists[0].name

        else:
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
        """
        downloads = File.objects.filter(folder=self.get_folder('downloads')).all()
        if len(downloads) < 1:
            return None
        return downloads
        """
    
    
    
    def get_download_url(self, format, version):
        
        return '%sdownload/%s/%s/' % (self.get_absolute_url(), format, version)
    
    
    
    
    
    
    
    def get_cache_file_path(self, format, version):
        
        tmp_directory = TEMP_DIR
        file_name = '%s_%s_%s.%s' % (format, version, str(self.uuid), 'zip')
        tmp_path = '%s/%s' % (tmp_directory, file_name)
        
        return tmp_path
    
    
    def clear_cache_file(self):
        """
        Clears cached release (the one for buy-downloads)
        """
        
        tmp_directory = TEMP_DIR
        pattern = '*%s.zip' % (str(self.uuid))
        versions = glob.glob('%s/%s' % (tmp_directory, pattern))
        
        print versions

        try:
            for version in versions:
                os.remove(version)
  
        except Exception, e:
            print e
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

            # archive_file.write('/Users/ohrstrom/code/alibrary/website/check.txt', 'test.txt')
            archive_file.write(media_cache_file.path, file_name)
                
            
        """
        adding assets if any
        asset_files = File.objects.filter(folder=self.get_folder('assets')).all()
        for asset_file in asset_files:
            if asset_file.name:
                file_name = asset_file.name
            else:
                file_name = asset_file.original_filename
            archive_file.write(asset_file.path, file_name)
        """

            
        return cache_file_path

    def get_extraimages(self):

        return None

        """
        if self.folder:
            folder = self.get_folder('pictures')
            images = folder.files.instance_of(Image)

        if len(images) > 0:
            return images
        else:
            return None
        """
                
                
    """
    def get_folder(self, name):
        
        if name == 'cache':
            parent_folder, created = Folder.objects.get_or_create(name='cache')
            folder, created = Folder.objects.get_or_create(name=str(self.uuid), parent=parent_folder)
        else:
            folder, created = Folder.objects.get_or_create(name=name, parent=self.folder)
            
        return folder
    """
    
    
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
        
        # update d_tags
        t_tags = ''
        for tag in self.tags:
            t_tags += '%s, ' % tag    
        
        self.tags = t_tags
        self.d_tags = t_tags
        

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

try:
    tagging.register(Release)
except:
    pass


arating.enable_voting_on(Release)
post_save.connect(library_post_save, sender=Release)  


""""""
from actstream import action
def action_handler(sender, instance, created, **kwargs):
    try:
        verb = _('updated')
        if created:
            verb = _('created')
        action.send(instance.get_last_editor(), verb=verb, target=instance)
    except Exception, e:
        print e

post_save.connect(action_handler, sender=Release)


class ReleaseExtraartists(models.Model):
    artist = models.ForeignKey('Artist', related_name='release_extraartist_artist')
    release = models.ForeignKey('Release', related_name='release_extraartist_release')
    profession = models.ForeignKey(Profession, verbose_name='Role/Profession', related_name='release_extraartist_profession', blank=True, null=True)   
    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')

""""""
class ReleaseAlbumartists(models.Model):
    artist = models.ForeignKey('Artist', related_name='release_albumartist_artist')
    release = models.ForeignKey('Release', related_name='release_albumartist_release')
    JOIN_PHRASE_CHOICES = (
        ('&', _('&')),
        (',', _(',')),
        ('and', _('and')),
        ('feat.', _('feat.')),
        ('vs.', _('vs.')),
        ('-', _('-')),
    )
    join_phrase = models.CharField(verbose_name="join phrase", max_length=12, default=None, choices=JOIN_PHRASE_CHOICES, blank=True, null=True)
    position = models.PositiveIntegerField(null=True, blank=True)
    
    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Albumartist')
        verbose_name_plural = _('Albumartists')
        ordering = ('position', )


class ReleaseRelations(models.Model):
    relation = models.ForeignKey('Relation', related_name='release_relation_relation')
    release = models.ForeignKey('Release', related_name='release_relation_release')
    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Relation')
        verbose_name_plural = _('Relations')
        

""""""
class ReleaseMedia(models.Model):
    release = models.ForeignKey('Release')
    media = models.ForeignKey('Media')
    position = models.PositiveIntegerField(null=True, blank=True)
    class Meta:
        app_label = 'alibrary'







        
class ReleasePlugin(CMSPlugin):
    
    release = models.ForeignKey(Release)
    def __unicode__(self):
        return self.release.name

    # meta
    class Meta:
        app_label = 'alibrary'
        
  
   
