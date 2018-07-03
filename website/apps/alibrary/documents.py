# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
elasticsearch index documents
"""

from elasticsearch_dsl import analyzer, tokenizer
from elasticsearch_dsl.serializer import serializer
from django_elasticsearch_dsl import DocType, Index, TextField, CompletionField, KeywordField, DateField, fields
from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.exceptions import InvalidImageFormatError
from .models import Artist, Label, Release, Media, Playlist

THUMBNAIL_OPT = dict(size=(197, 197), crop=True, upscale=True)

library_index = Index('library')
artist_index = Index('artists')
label_index = Index('labels')
release_index = Index('releases')
media_index = Index('media')

# autocomplete tokenizer
edge_ngram_tokenizer = tokenizer(
    'edge_ngram_tokenizer',
    type='edge_ngram',
    min_gram=1,
    max_gram=12,
    # TODO: investigate
    token_chars=['letter', 'digit']
)


# keyword_analyzer = analyzer(
#     'keyword_analyzer',
#     tokenizer="keyword",
#     filter=["lowercase", "asciifolding", "trim"],
#     type='custom',
#     char_filter=[]
# )

# autocomplete analyzer
edge_ngram_analyzer = analyzer(
    'edge_ngram_analyzer',
    tokenizer=edge_ngram_tokenizer,
    filter=['lowercase', 'asciifolding'],
)

# autocomplete *search* analyzer
edge_ngram_search_analyzer = analyzer(
    'edge_ngram_search_analyzer',
    tokenizer='lowercase',
)


# asciifolding analyzer
asciifolding_analyzer = analyzer(
    'asciifolding_analyzer',
    tokenizer='standard',
    filter=['lowercase', 'asciifolding'],
)


class LibraryBaseDocument(object):
    pass


@label_index.doc_type
class LabelDocument(LibraryBaseDocument, DocType):

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

    name = fields.TextField(fielddata=True)
    exact_name = fields.KeywordField(attr='name')
    tags = KeywordField()
    labelcode = KeywordField()

    # tags = fields.NestedField(properties={
    #     'name': fields.KeywordField(),
    #     'id': fields.IntegerField(),
    # })


    image = KeywordField()

    type = fields.KeywordField()

    year_start = fields.IntegerField()
    year_end = fields.IntegerField()

    description = fields.TextField(attr='description')
    country = KeywordField(attr='country.iso2_code')


    ###################################################################
    # field preparation
    ###################################################################
    def prepare_autocomplete(self, instance):
        text = [instance.name.strip()]
        # TODO: check what exact fields needed
        if instance.parent:
            text += [instance.parent.name.strip()]
        if instance.get_root():
            text += [instance.get_root().name.strip()]
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
            except InvalidImageFormatError:
                pass


    def prepare_year_start(self, instance):
        if instance.date_start:
            return instance.date_start.year

    def prepare_year_end(self, instance):
        if instance.date_end:
            return instance.date_end.year

    ###################################################################
    # custom queryset
    ###################################################################
    def get_queryset(self):
        return super(LabelDocument, self).get_queryset().select_related('country', 'parent')


@artist_index.doc_type
class ArtistDocument(LibraryBaseDocument, DocType):

    class Meta:
        model = Artist
        queryset_pagination = 1000
        doc_type = 'alibrary.artist'

    autocomplete = fields.TextField(
        analyzer=edge_ngram_analyzer,
        search_analyzer=edge_ngram_search_analyzer,
    )

    url = fields.KeywordField(attr='get_absolute_url')
    api_url = fields.KeywordField(attr='get_api_url')
    created = fields.DateField()
    updated = fields.DateField()

    # 'fielddata' is needed for sorting on the filed
    name = fields.TextField(fielddata=True)
    real_name = fields.TextField()
    namevariations = fields.TextField()
    tags = KeywordField()

    image = KeywordField()

    type = fields.KeywordField()
    ipi_code = fields.KeywordField()
    isni_code = fields.KeywordField()

    year_start = fields.IntegerField()
    year_end = fields.IntegerField()

    description = fields.TextField(attr='biography')
    country = KeywordField(attr='country.iso2_code')


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

    ###################################################################
    # field preparation
    ###################################################################
    def prepare_autocomplete(self, instance):
        text = [instance.name.strip()]
        text += [i.name.strip() for i in instance.namevariations.all()]
        return text

    def prepare_name(self, instance):
        return instance.name.strip()

    def prepare_namevariations(self, instance):
        return [i.name.strip() for i in instance.namevariations.all()]

    def prepare_tags(self, instance):
        return [i.strip() for i in instance.d_tags.split(',') if len(i) > 2]
        #return [{'id': i.pk, 'name': i.name} for i in instance.tags.all()]

    def prepare_image(self, instance):
        if hasattr(instance, 'main_image') and instance.main_image:
            try:
                return get_thumbnailer(instance.main_image).get_thumbnail(THUMBNAIL_OPT).url
            except InvalidImageFormatError:
                pass

    def prepare_year_start(self, instance):
        if instance.date_start:
            return instance.date_start.year

    def prepare_year_end(self, instance):
        if instance.date_end:
            return instance.date_end.year

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
class ReleaseDocument(LibraryBaseDocument, DocType):

    class Meta:
        model = Release
        queryset_pagination = 1000
        doc_type = 'alibrary.release'

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
    # name = fields.TextField(
    #     analyzer=asciifolding_analyzer,
    #     fielddata=True
    # )
    tags = KeywordField()

    image = KeywordField()

    type = fields.KeywordField(attr='releasetype')
    barcode = fields.KeywordField()

    description = fields.TextField()
    country = KeywordField(attr='release_country.iso2_code')

    num_media = fields.IntegerField()

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
            except InvalidImageFormatError:
                pass

    def prepare_num_media(self, instance):
        return instance.media_release.count()

    ###################################################################
    # custom queryset
    ###################################################################
    def get_queryset(self):
        return super(ReleaseDocument, self).get_queryset().all().select_related(
            'release_country'
        ).prefetch_related('media_release')



@media_index.doc_type
class MediaDocument(LibraryBaseDocument, DocType):

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
        fielddata=True
    )

    tags = KeywordField()
    image = KeywordField()

    type = fields.KeywordField(attr='mediatype')
    #barcode = fields.KeywordField()

    description = fields.TextField()
    lyrics = fields.TextField()
    #country = KeywordField(attr='release_country.iso2_code')

    #num_media = fields.IntegerField()

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
        if hasattr(instance, 'release') and hasattr(instance.release, 'main_image'):
            try:
                return get_thumbnailer(instance.release.main_image).get_thumbnail(THUMBNAIL_OPT).url
            except InvalidImageFormatError:
                pass

    def prepare_num_media(self, instance):
        return instance.media_release.count()

    ###################################################################
    # custom queryset
    ###################################################################
    def get_queryset(self):
        return super(MediaDocument, self).get_queryset().all().select_related(
            'release', 'artist', 'license'
        )
