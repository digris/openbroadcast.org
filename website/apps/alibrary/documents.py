# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
elasticsearch index documents
"""

from django_elasticsearch_dsl import DocType, Index, KeywordField, fields
from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.exceptions import InvalidImageFormatError
from search.elasticsearch_utils import edge_ngram_analyzer, edge_ngram_search_analyzer

from importer.util.importitem import get_import_sessions_for_obj

from .models import Artist, Label, Release, Media, Playlist, Series

THUMBNAIL_OPT = dict(size=(197, 197), crop=True, upscale=True)

library_index = Index('library')
artist_index = Index('artists')
label_index = Index('labels')
release_index = Index('releases')
media_index = Index('media')

@label_index.doc_type
class LabelDocument(DocType):

    class Meta:
        model = Label
        queryset_pagination = 1000
        doc_type = 'alibrary.label'

    autocomplete = fields.TextField(
        analyzer=edge_ngram_analyzer,
        search_analyzer=edge_ngram_search_analyzer,
    )

    url = fields.KeywordField(attr='get_absolute_url')
    api_url = fields.KeywordField(attr='get_api_url')
    created = fields.DateField()
    updated = fields.DateField()

    name = fields.TextField(
        fielddata=True,
        fields={
            'raw': {'type': 'keyword'}
        }
    )
    # TODO: remove 'exact_name' from index/document
    exact_name = fields.KeywordField(attr='name')
    tags = KeywordField()
    labelcode = KeywordField()

    # tags = fields.NestedField(properties={
    #     'name': fields.KeywordField(),
    #     'id': fields.IntegerField(),
    # })

    creator = fields.KeywordField(attr='creator.username')


    image = KeywordField()

    type = fields.KeywordField(attr='get_type_display')

    year_start = fields.IntegerField()
    year_end = fields.IntegerField()

    description = fields.TextField(attr='description')
    country = KeywordField(attr='country.printable_name')
    country_code = KeywordField(attr='country.iso2_code')

    import_ids = fields.KeywordField()

    ###################################################################
    # field preparation
    ###################################################################
    def prepare_autocomplete(self, instance):
        text = [instance.name.strip()]
        # TODO: check what exact fields needed
        # if instance.labelcode:
        #     text += [instance.labelcode.strip()]
        # if instance.get_root():
        #     text += [instance.get_root().name.strip()]
        # if instance.parent:
        #     text += [instance.parent.name.strip()]
        if instance.country:
            text += [instance.country.iso2_code]

        return text

    def prepare_name(self, instance):
        return instance.name.strip()

    def prepare_tags(self, instance):
        return [i.strip() for i in instance.d_tags.split(',') if len(i) > 2]
        #return [{'id': i.pk, 'name': i.name} for i in instance.tags.all()]

    def prepare_image(self, instance):
        if hasattr(instance, 'main_image') and instance.main_image:
            try:
                return get_thumbnailer(instance.main_image).get_thumbnail(THUMBNAIL_OPT).url
            except (InvalidImageFormatError, AttributeError):
                pass


    def prepare_year_start(self, instance):
        if instance.date_start:
            return instance.date_start.year

    def prepare_year_end(self, instance):
        if instance.date_end:
            return instance.date_end.year

    def prepare_import_ids(self, instance):
        ids = [str(i.uuid) for i in get_import_sessions_for_obj(instance)]
        return list(set(ids))

    ###################################################################
    # custom queryset
    ###################################################################
    def get_queryset(self):
        return super(LabelDocument, self).get_queryset().select_related('country', 'parent')


@artist_index.doc_type
class ArtistDocument(DocType):

    class Meta:
        model = Artist
        queryset_pagination = 1000
        doc_type = 'alibrary.artist'

    autocomplete = fields.TextField(
        analyzer=edge_ngram_analyzer,
        search_analyzer=edge_ngram_search_analyzer,
    )

    # id = fields.IntegerField()

    url = fields.KeywordField(attr='get_absolute_url')
    api_url = fields.KeywordField(attr='get_api_url')
    created = fields.DateField()
    updated = fields.DateField()

    # 'fielddata' is needed for sorting on the filed
    name = fields.TextField(
        fielddata=True,
        fields={
            'raw': {'type': 'keyword'}
        }
    )
    real_name = fields.TextField(
        fields={
            'raw': {'type': 'keyword'}
        }
    )
    namevariations = fields.TextField()
    tags = KeywordField()

    creator = fields.KeywordField(attr='creator.username')

    image = KeywordField()

    type = fields.KeywordField(attr='get_type_display')
    ipi_code = fields.KeywordField()
    isni_code = fields.KeywordField()

    year_start = fields.IntegerField()
    year_end = fields.IntegerField()

    description = fields.TextField(attr='biography')
    country = KeywordField(attr='country.printable_name')
    country_code = KeywordField(attr='country.iso2_code')


    ###################################################################
    # relation fields
    ###################################################################
    aliases = fields.NestedField(properties={
        'name': fields.TextField(),
        'real_name': fields.TextField(),
        'pk': fields.IntegerField(),
    })
    members = fields.NestedField(properties={
        'name': fields.TextField(),
        'real_name': fields.TextField(),
        'pk': fields.IntegerField(),
    })

    import_ids = fields.KeywordField()

    ###################################################################
    # field preparation
    ###################################################################
    def prepare_autocomplete(self, instance):
        text = [instance.name.strip()]
        text += [i.name.strip() for i in instance.namevariations.nocache().all()]
        return text

    def prepare_name(self, instance):
        return instance.name.strip()

    def prepare_namevariations(self, instance):
        return [i.name.strip() for i in instance.namevariations.nocache().all()]

    def prepare_tags(self, instance):
        return [i.strip() for i in instance.d_tags.split(',') if len(i) > 2]
        #return [{'id': i.pk, 'name': i.name} for i in instance.tags.all()]

    def prepare_image(self, instance):
        if hasattr(instance, 'main_image') and instance.main_image:
            try:
                return get_thumbnailer(instance.main_image).get_thumbnail(THUMBNAIL_OPT).url
            except (InvalidImageFormatError, AttributeError):
                pass

    def prepare_year_start(self, instance):
        if instance.date_start:
            return instance.date_start.year

    def prepare_year_end(self, instance):
        if instance.date_end:
            return instance.date_end.year

    def prepare_import_ids(self, instance):
        ids = [str(i.uuid) for i in get_import_sessions_for_obj(instance)]
        return list(set(ids))

    ###################################################################
    # custom queryset
    ###################################################################
    def get_queryset(self):
        return super(ArtistDocument, self).get_queryset().filter(listed=True).select_related(
            'country'
        ).prefetch_related(
            'aliases', 'members'
        )



@release_index.doc_type
class ReleaseDocument(DocType):

    class Meta:
        model = Release
        queryset_pagination = 1000
        doc_type = 'alibrary.release'

    autocomplete = fields.TextField(
        analyzer=edge_ngram_analyzer,
        search_analyzer=edge_ngram_search_analyzer,
    )

    # id = fields.IntegerField()

    url = fields.KeywordField(attr='get_absolute_url')
    api_url = fields.KeywordField(attr='get_api_url')
    created = fields.DateField()
    updated = fields.DateField()

    # 'fielddata' is needed for sorting on the filed
    name = fields.TextField(
        fielddata=True,
        fields={
            'raw': {'type': 'keyword'}
        }
    )

    artist_display = fields.KeywordField(
        attr='get_artist_display',
        fields={
            'raw': {'type': 'keyword'}
        }
    )

    label_display = fields.KeywordField(
        attr='label.name',
        fields={
            'raw': {'type': 'keyword'}
        }
    )

    # name = fields.TextField(
    #     analyzer=asciifolding_analyzer,
    #     fielddata=True
    # )
    tags = KeywordField()

    creator = fields.KeywordField(attr='creator.username')

    image = KeywordField()

    type = fields.KeywordField(attr='get_releasetype_display')
    label_type = fields.KeywordField(attr='label.get_type_display')
    barcode = fields.KeywordField()

    releasedate_year = fields.IntegerField()
    catalognumber = fields.KeywordField()

    description = fields.TextField()
    country = KeywordField(attr='release_country.printable_name')
    country_code = KeywordField(attr='release_country.iso2_code')

    num_media = fields.IntegerField()

    artist_ids = fields.KeywordField()
    label_ids = fields.KeywordField()
    import_ids = fields.KeywordField()

    ###################################################################
    # field preparation
    ###################################################################
    def prepare_autocomplete(self, instance):
        text = [instance.name.strip()]
        return text

    def prepare_name(self, instance):
        return instance.name.strip()

    def prepare_tags(self, instance):
        return [i.strip() for i in instance.d_tags.split(',') if len(i) > 2]
        #return [{'id': i.pk, 'name': i.name} for i in instance.tags.all()]

    def prepare_image(self, instance):
        if hasattr(instance, 'main_image') and instance.main_image:
            try:
                return get_thumbnailer(instance.main_image).get_thumbnail(THUMBNAIL_OPT).url
            except (InvalidImageFormatError, AttributeError):
                pass

    def prepare_num_media(self, instance):
        return instance.media_release.count()

    def prepare_releasedate_year(self, instance):
        if instance.releasedate:
            return instance.releasedate.year

    # add all related (appearing artist, extra artist) (uu)ids to the document
    def prepare_artist_ids(self, instance):
        ids = []
        for media in instance.get_media():
            ids += [str(media.artist.uuid)]
        for artist in instance.album_artists.all():
            ids += [str(artist.uuid)]
        for artist in instance.extra_artists.all():
            ids += [str(artist.uuid)]
        return list(set(ids))

    # add related label ids (in this case only one, but keep it as a list for consistency)
    def prepare_label_ids(self, instance):
        ids = []
        if instance.label:
            ids += [str(instance.label.uuid)]
        return list(set(ids))

    def prepare_import_ids(self, instance):
        ids = [str(i.uuid) for i in get_import_sessions_for_obj(instance)]
        return list(set(ids))

    ###################################################################
    # custom queryset
    ###################################################################
    def get_queryset(self):
        return super(ReleaseDocument, self).get_queryset().all().select_related(
            'release_country'
        ).prefetch_related(
            'media_release',
            'extra_artists',
            'album_artists',
        )



@media_index.doc_type
class MediaDocument(DocType):

    class Meta:
        model = Media
        queryset_pagination = 1000
        doc_type = 'alibrary.media'

    autocomplete = fields.TextField(
        analyzer=edge_ngram_analyzer,
        search_analyzer=edge_ngram_search_analyzer,
    )

    url = fields.KeywordField(attr='get_absolute_url')
    api_url = fields.KeywordField(attr='get_api_url')
    created = fields.DateField()
    updated = fields.DateField()

    # 'fielddata' is needed for sorting on the filed
    name = fields.TextField(
        fielddata=True,
        fields={
            'raw': {'type': 'keyword'}
        }
    )

    artist_display = fields.KeywordField(
        attr='get_artist_display',
        fields={
            'raw': {'type': 'keyword'}
        }
    )
    release_display = fields.KeywordField(
        attr='release.name',
        fields={
            'raw': {'type': 'keyword'}
        }
    )

    tags = KeywordField()

    # id = fields.IntegerField()

    creator = fields.KeywordField(attr='creator.username')

    image = KeywordField()

    type = fields.KeywordField(attr='get_mediatype_display')
    version = fields.KeywordField(attr='get_version_display')
    #barcode = fields.KeywordField()

    description = fields.TextField()
    lyrics = fields.TextField()
    lyrics_language = fields.KeywordField(attr='get_lyrics_language_display')
    #country = KeywordField(attr='release_country.iso2_code')

    # audio-properties
    duration = fields.IntegerField(attr='master_duration')
    bitrate = fields.IntegerField(attr='master_bitrate')
    samplerate = fields.IntegerField(attr='master_samplerate')
    encoding = fields.KeywordField(attr='master_encoding')
    tempo = fields.FloatField(attr='tempo')

    # license = fields.NestedField(properties={
    #     'name': fields.KeywordField(),
    #     'id': fields.IntegerField(),
    # })

    license = fields.KeywordField()

    last_emission = fields.DateField()
    num_emissions = fields.IntegerField()

    artist_ids = fields.KeywordField()
    release_ids = fields.KeywordField()
    import_ids = fields.KeywordField()

    ###################################################################
    # field preparation
    ###################################################################
    def prepare_autocomplete(self, instance):
        text = [instance.name.strip()]
        text += [instance.get_artist_display()]
        if instance.release:
            text += [instance.release.name]
        return text

    def prepare_name(self, instance):
        return instance.name.strip()

    def prepare_tags(self, instance):
        return [i.strip() for i in instance.d_tags.split(',') if len(i) > 2]
        #return [{'id': i.pk, 'name': i.name} for i in instance.tags.all()]

    def prepare_image(self, instance):
        if hasattr(instance, 'release') and hasattr(instance.release, 'main_image'):
            try:
                return get_thumbnailer(instance.release.main_image).get_thumbnail(THUMBNAIL_OPT).url
            except (InvalidImageFormatError, AttributeError):
                pass

    def prepare_license(self, instance):

        if instance.license:
            return instance.license.title
            # return {
            #     'id': instance.license.pk,
            #     'name': instance.license.name,
            # }

    def prepare_last_emission(self, instance):
        if instance.last_emission:
            return instance.last_emission.time_start

    def prepare_num_emissions(self, instance):
        qs = instance.emissions
        return qs.count()

    def prepare_encoding(self, instance):
        if instance.master_encoding:
            return instance.master_encoding.upper()


    # add all related (appearing artist, extra artist) (uu)ids to the document
    def prepare_artist_ids(self, instance):
        ids = []
        if instance.artist:
            ids += [str(instance.artist.uuid)]
        for artist in instance.media_artists.all():
            ids += [str(artist.uuid)]
        for artist in instance.extra_artists.all():
            ids += [str(artist.uuid)]
        return list(set(ids))

    # add related release ids (in this case only one, but keep it as a list for consistency)
    def prepare_release_ids(self, instance):
        ids = []
        if instance.release:
            ids += [str(instance.release.uuid)]
        return list(set(ids))

    def prepare_import_ids(self, instance):
        ids = [str(i.uuid) for i in get_import_sessions_for_obj(instance)]
        return list(set(ids))


    ###################################################################
    # custom queryset
    ###################################################################
    def get_queryset(self):
        return super(MediaDocument, self).get_queryset().all().select_related(
            'release', 'artist', 'license'
        ).prefetch_related(
            'media_artists', 'extra_artists'
        )




playlist_index = Index('playlists')

@playlist_index.doc_type
class PlaylistDocument(DocType):

    class Meta:
        model = Playlist
        queryset_pagination = 1000
        doc_type = 'alibrary.playlist'

    autocomplete = fields.TextField(
        analyzer=edge_ngram_analyzer,
        search_analyzer=edge_ngram_search_analyzer,
    )

    url = fields.KeywordField(attr='get_absolute_url')
    api_url = fields.KeywordField(attr='get_api_url')
    created = fields.DateField()
    updated = fields.DateField()

    # 'fielddata' is needed for sorting on the filed
    name = fields.TextField(
        fielddata=True
    )
    tags = KeywordField()

    user = fields.KeywordField(attr='user.username')

    image = KeywordField()

    type = fields.KeywordField(attr='get_type_display')
    status = fields.KeywordField(attr='get_status_display')
    target_duration = fields.KeywordField()
    weather = fields.KeywordField()
    seasons = fields.KeywordField()
    series = fields.KeywordField()
    daypart_days = fields.KeywordField()
    daypart_slots = fields.KeywordField()

    description = fields.TextField()

    last_emission = fields.DateField()
    num_emissions = fields.IntegerField()
    state_flags = fields.KeywordField()


    ###################################################################
    # field preparation
    ###################################################################
    def prepare_autocomplete(self, instance):
        # if instance.type == 'basket':
        #     return
        text = [instance.name.strip()]
        if instance.series and instance.series_number:
            text += ['{} #{}'.format(instance.series, instance.series_number)]
        elif instance.series:
            text += [instance.series.name]
        return text

    def prepare_name(self, instance):
        return instance.name.strip()

    def prepare_tags(self, instance):
        return [i.strip() for i in instance.d_tags.split(',') if len(i) > 2]
        #return [{'id': i.pk, 'name': i.name} for i in instance.tags.all()]

    def prepare_image(self, instance):
        if hasattr(instance, 'main_image') and instance.main_image:
            try:
                return get_thumbnailer(instance.main_image).get_thumbnail(THUMBNAIL_OPT).url
            except (InvalidImageFormatError, AttributeError):
                pass

    def prepare_target_duration(self, instance):
        if instance.target_duration:
            return '{} Minutes'.format(instance.get_target_duration_display())
        return


    def prepare_series(self, instance):
        if instance.series and instance.series_number:
            return '{} #{}'.format(instance.series, instance.series_number)
        elif instance.series:
            return instance.series.name
        return

    def prepare_last_emission(self, instance):
        if instance.last_emission:
            return instance.last_emission.time_start

    def prepare_num_emissions(self, instance):
        return instance.get_emissions().count()

    def prepare_weather(self, instance):
        return [w.name.strip() for w in instance.weather.all()]

    def prepare_seasons(self, instance):
        return [s.name.strip() for s in instance.seasons.all()]

    def prepare_daypart_days(self, instance):
        return [d.get_day_display() for d in instance.dayparts.all()]

    def prepare_daypart_slots(self, instance):
        return ['{:%H} - {:%H}h'.format(d.time_start, d.time_end) for d in instance.dayparts.all()]

    def prepare_state_flags(self, instance):
        flags = []
        if instance.is_archived:
            flags += ['Archived - Yes']
        elif instance.type == 'broadcast':
            flags += ['Archived - No']
        if instance.rotation:
            flags += ['In Rotation - Yes']
        elif instance.type == 'broadcast':
            flags += ['In Rotation - No']

        return flags


    # ###################################################################
    # # custom queryset
    # ###################################################################
    # def get_queryset(self):
    #     return super(PlaylistDocument, self).get_queryset().exclude(type='basket')




series_index = Index('series')

@series_index.doc_type
class SeriesDocument(DocType):

    class Meta:
        model = Series
        queryset_pagination = 1000
        doc_type = 'alibrary.series'

    autocomplete = fields.TextField(
        analyzer=edge_ngram_analyzer,
        search_analyzer=edge_ngram_search_analyzer,
    )

    name = fields.TextField(
        fielddata=True
    )

    ###################################################################
    # field preparation
    ###################################################################
    def prepare_autocomplete(self, instance):
        text = [instance.name.strip()]
        return text

    def prepare_name(self, instance):
        return instance.name.strip()
