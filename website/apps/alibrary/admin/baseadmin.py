from multilingual.admin import MultilingualModelAdmin
from genericadmin.admin import GenericAdminModelAdmin, GenericTabularInline
import reversion
from guardian.admin import GuardedModelAdmin

from django.contrib import admin

from ashop.models import *
from alibrary.models import *

from django.utils.safestring import mark_safe
from django.shortcuts import render_to_response
from django.template import RequestContext

#class BaseAdmin(reversion.VersionAdmin, GuardedModelAdmin):
class BaseAdmin(GuardedModelAdmin):

    search_fields = ['name']
    save_on_top = True
    
    
class HardwarereleaseInline(admin.TabularInline):
    max_num = 10
    model = Hardwarerelease
    fieldsets = [
        (None,               {'fields': ['name', 'slug', 'medium', 'unit_price', 'active']}),
    ]
    readonly_fields = ['slug', 'medium']
    
class DownloadreleaseInline(admin.TabularInline):
    max_num = 1
    model = Downloadrelease
    fieldsets = [
        (None,               {'fields': ['name', 'slug', 'unit_price', 'active']}),
    ]
    readonly_fields = ['slug', 'name', 'unit_price']

class LabelInline(admin.TabularInline):
    model = Label
    extra = 1

class MediaInline(admin.TabularInline):
    model = Media
    exclude = ['description','slug','processed','echoprint_status','conversion_status', 'd_tags', 'echonest_id', 'lyrics', 'lyrics_language', 'danceability', 'energy', 'liveness', 'loudness', 'speechiness', 'start_of_fade_out', 'echonest_duration', 'tempo', 'key', 'sections','master_sha1', 'base_format', 'base_filesize', 'base_duration', 'base_samplerate', 'base_bitrate', 'filename', 'publish_date', 'status', 'owner', 'creator', 'publisher', 'medianumber', 'master', 'mediatype' ]
    readonly_fields = ['artist', ]
    extra = 0
    
class FormatAdmin(BaseAdmin):
    
    list_display   = ('format', 'version', 'default_price')

    fieldsets = [
        (None,               {'fields': ['format', 'version', 'default_price', 'excerpt']}),
    ]
    
admin.site.register(Format, FormatAdmin)
    
    
class ReleaseExtraartistsInline(admin.TabularInline):
    model = ReleaseExtraartists
    extra=1   
    
    
class ReleaseAlbumartistsInline(admin.TabularInline):
    model = ReleaseAlbumartists
    extra=2
    fieldsets = [
        (None,               {'fields': ['position', 'join_phrase', 'artist']}),
    ]
   

class RelationsInline(GenericTabularInline):
    model = Relation
    extra=2
    fieldsets = [
        (None,               {'fields': ['url', 'name', 'service']}),
    ]
    readonly_fields = ['service']

    
#class ReleaseAdmin(PlaceholderAdmin, BaseAdmin):

class ReleaseMediaMediaInline(admin.TabularInline):
    model = Media
    extra = 1


class ReleaseMediaInline(admin.TabularInline):
    model = ReleaseMedia
    extra = 1 
    inlines = [ReleaseMediaMediaInline]

class ReleaseAdmin(BaseAdmin):

    list_display   = ('name', 'releasetype', 'label', 'slug', 'uuid', 'catalognumber',)
    search_fields = ['name', 'label__name',]
    list_filter = ('releasetype',)
    date_hierarchy = 'created'

    inlines = [ReleaseAlbumartistsInline, MediaInline, RelationsInline, ReleaseExtraartistsInline]
    readonly_fields = ['slug', 'license', 'd_tags']

    fieldsets = [
        (None,  {
                'fields': ['name', 'slug', 'main_image', ('label', 'catalognumber'), ('releasedate', 'release_country', 'license'), ('releasetype',), 'enable_comments', 'main_format', 'd_tags', 'description']
                }),
        ('Users', {'fields' : ['owner', 'creator', 'publisher']}),
    ]
    
#admin.site.register(Release)
admin.site.register(Release, ReleaseAdmin)



class ArtistMembersInline(admin.TabularInline):
    model = Artist.members.through
    fk_name = 'parent'
    extra=1
    
class ArtistParentsInline(admin.TabularInline):
    model = Artist.members.through
    fk_name = 'child'
    extra=1
    
class ArtistProfessionsInline(admin.TabularInline):
    model = ArtistProfessions
    extra=1
    
class MediaExtraartistsInline(admin.TabularInline):
    model = MediaExtraartists
    extra=1


class AgencyArtistInline(admin.TabularInline):
    model = Agency.artists.through
    extra = 1


class NameVariationInline(admin.TabularInline):
    model = NameVariation
    extra = 3
         
class ArtistAdmin(BaseAdmin):

    list_display   = ('name', 'type', 'disambiguation', 'listed',)
    search_fields = ['name', 'media__name',]
    list_filter = ('listed',)
    
    # RelationsInline, 
    inlines = [NameVariationInline, RelationsInline, ArtistProfessionsInline, ArtistMembersInline, ArtistParentsInline, AgencyArtistInline]
    
    readonly_fields = ["folder",]
    
    """"""
    fieldsets = [
        (None,               {'fields': ['name', 'slug', 'main_image', 'real_name', 'country', ('listed', 'disable_link',), 'enable_comments', 'biography', 'excerpt', 'folder', ]}),
        ('Users', {'fields' : ['owner', 'creator', 'publisher']}),
        ('Various', {'fields' : ['booking_contact', 'email',]}),
    ]
    
admin.site.register(Artist, ArtistAdmin)
admin.site.register(NameVariation)

class LicenseAdmin(reversion.VersionAdmin, MultilingualModelAdmin):
    
    inline_instances = ('name_translated', 'restricted', 'parent',)
    
    list_display   = ('name', 'parent', 'legacy_id', 'key', 'restricted', 'selectable', 'is_default',)
    search_fields = ('name',)
    
admin.site.register(License, LicenseAdmin)
      
      
      
      
class ServiceAdmin(BaseAdmin):
    pass
    
admin.site.register(Service, ServiceAdmin)      
      
      
class RelationAdmin(BaseAdmin):

    list_display = ('url', 'service', 'name',)
    list_filter = ('service',)
    search_fields = ('url',)
    fieldsets = [
        (None,               {'fields': ['url', 'service']}),
    ]
    #readonly_fields = ['service']
    
admin.site.register(Relation, RelationAdmin)
      
class ProfessionAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Profession, ProfessionAdmin)


""""""
class MediaReleaseInline(admin.TabularInline):
    model = Release.media.through
    extra = 1

    
class MediaAdmin(BaseAdmin):
    
    list_display   = ('name', 'created', 'release_link', 'artist', 'mediatype', 'tracknumber', 'medianumber', 'duration', 'processed', 'echoprint_status', 'conversion_status',)
    search_fields = ['artist__name', 'release__name', 'name']
    list_filter = ('mediatype', 'license__name', 'processed', 'echoprint_status', 'conversion_status')
    
    inlines = [MediaReleaseInline, RelationsInline, MediaExtraartistsInline]

    readonly_fields = ['slug', 'folder', 'uuid', 'base_format', 'base_filesize', 'base_duration','base_samplerate', 'base_bitrate', 'release_link', 'master_sha1', 'd_tags']


    date_hierarchy = 'created'
    
    """"""
    fieldsets = [
        (None,  {'fields': 
                 ['name', 'slug', 'isrc', 'filename', 'uuid', ('tracknumber', 'medianumber', 'opus_number'), 'mediatype', 'version', ('release', 'release_link'), 'artist', 'license', 'd_tags', 'echonest_id',]
                 }),
                 
        ('Users', {'fields' : ['owner', 'creator', 'publisher']}),
        ('Text', {'fields' : ['description', 'lyrics',]}),
                 
        ('Storage related',  {
                'fields': ['master', 'master_sha1', 'folder', ('base_format', 'base_filesize', 'base_duration',), ('base_samplerate', 'base_bitrate')]
                 }),

        #('Mixed content', {'fields': ['description'], 'classes': ['']}),
        ('Advanced options [Know what you are doing!!!!!!!!]', {
            'classes': ('uncollapse',),
            'fields': ('processed','echoprint_status','conversion_status',)
        }),
    ]
    
    
admin.site.register(Media, MediaAdmin)
    
    
class DistributorLabelInline(admin.TabularInline):
    model = Distributor.labels.through
    extra = 1
    
class LabelAdmin(BaseAdmin):
    
    # inlines = [LabelInline]
    #prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ['slug']
    
    inlines = [RelationsInline]
    
    """"""
    fieldsets = [
        (None,               {'fields': ['name', 'slug', 'type', 'description']}),
        ('Contact', {'fields' : ['address', 'country', ('phone', 'fax'), 'email']}),
        ('Settings', {'fields' : ['listed', 'disable_link', 'disable_editing']}),
        ('Relations', {'fields': ['parent',], 'classes': ['']}),
        ('Users', {'fields' : [('owner', 'creator', 'publisher'),]}),
    ]
    
admin.site.register(Label, LabelAdmin)
    
class DistributorAdmin(BaseAdmin):
    
    # inlines = [LabelInline]
    #prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ['slug', 'd_tags']
    
    inlines = [DistributorLabelInline, RelationsInline]
    
    """"""
    fieldsets = [
        (None,               {'fields': ['name', 'slug', 'type', 'description']}),
        ('Contact', {'fields' : ['address', 'country', ('phone', 'fax'), 'email']}),
        ('Relations', {'fields': ['parent'], 'classes': ['']}),
        ('Users', {'fields' : [('owner', 'creator', 'publisher'),]}),
    ]
    
admin.site.register(Distributor, DistributorAdmin)



class AgencyAdmin(BaseAdmin):

    # inlines = [LabelInline]
    #prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ['slug', 'd_tags']

    inlines = [AgencyArtistInline, RelationsInline]

    fieldsets = [
        (None,               {'fields': ['name', 'slug', 'type', 'description']}),
        ('Contact', {'fields' : ['address', 'country', ('phone', 'fax'), 'email']}),
        ('Relations', {'fields': ['parent'], 'classes': ['']}),
        ('Users', {'fields' : [('owner', 'creator', 'publisher'),]}),
    ]

admin.site.register(Agency, AgencyAdmin)
admin.site.register(AgencyScope)


    
class PlaylistmediaInline(GenericTabularInline):
    model = PlaylistMedia
    extra=1
    
class PlaylistItemInline(GenericTabularInline):
    model = PlaylistItem
    extra=1
    
class PlaylistItemPlaylistInline(admin.TabularInline):
    model = PlaylistItemPlaylist
    inlines = [PlaylistItemInline,] 
    extra=1
        
class PlaylistAdmin(GenericAdminModelAdmin):
    
    list_display   = ('name', 'user', 'type', 'duration', 'target_duration', 'is_current', 'rotation', 'updated')
    list_filter = ('type', 'broadcast_status', )

    search_fields = ['name', 'user__username',]
    date_hierarchy = 'created'
    
    #readonly_fields = ['slug', 'is_current',]

    inlines = [PlaylistItemPlaylistInline] 
 
class PlaylistItemAdmin(GenericAdminModelAdmin):
    pass
        
class DaypartAdmin(BaseAdmin):
    
    list_display   = ('day', 'time_start', 'time_end', 'active', 'playlist_count',)
    list_filter = ('day', 'active',)


    
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Daypart, DaypartAdmin)
admin.site.register(PlaylistItem, PlaylistItemAdmin)


        
class MediaformatAdmin(BaseAdmin):
    pass
    
admin.site.register(Mediaformat, MediaformatAdmin)



admin.site.register(APILookup)


from modeltranslation.admin import TranslationAdmin
class SeasonAdmin(TranslationAdmin):
    pass
class WeatherAdmin(TranslationAdmin):
    pass

admin.site.register(Season, SeasonAdmin)
admin.site.register(Weather, WeatherAdmin)

admin.site.register(Series)




"""
from tastypie.admin import ApiKeyInline
from tastypie.models import ApiAccess, ApiKey
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.register(ApiKey)
admin.site.register(ApiAccess)


class UserModelAdmin(UserAdmin):
    inlines = UserAdmin.inlines + [ApiKeyInline]

admin.site.unregister(User)
admin.site.register(User,UserModelAdmin)
"""


