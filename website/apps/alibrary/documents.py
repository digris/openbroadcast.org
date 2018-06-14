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
from .models import Artist, Label

THUMBNAIL_OPT = dict(size=(197, 197), crop=True, upscale=True)

library_index = Index('library')
artist_index = Index('artists')
label_index = Index('labels')


# @artist_index.doc_type
# class ArtistDocument(DocType):
#
#     aliases = TextField()
#     members = TextField()
#     tags = KeywordField()
#     country = KeywordField(attr='country.iso2_code')
#
#     description = TextField(attr='biography')
#
#     # date_start = DateField(attr='date_start')
#     # date_end = DateField(attr='date_end')
#
#     #name_suggest = CompletionField(attr='name')
#
#     def prepare_aliases(self, instance):
#         return [i.name for i in instance.aliases.all()]
#
#     def prepare_tags(self, instance):
#         return [i.name for i in instance.tags.all()]
#
#     def prepare_members(self, instance):
#         return [i.name for i in instance.members.all()]
#
#     class Meta:
#         model = Artist
#         queryset_pagination = 1000
#         doc_type = 'alibrary.artist'
#
#         fields = [
#             'name',
#             'real_name',
#             'type',
#         ]


edge_ngram_tokenizer = tokenizer(
    'edge_ngram_tokenizer',
    type='edge_ngram',
    min_gram=1,
    max_gram=12,
    token_chars=['letter']
)


keyword_analyzer = analyzer(
    'keyword_analyzer',
    tokenizer="keyword",
    filter=["lowercase", "asciifolding", "trim"],
    type='custom',
    char_filter=[]
)

edge_ngram_analyzer = analyzer(
    'edge_ngram_analyzer',
    tokenizer=edge_ngram_tokenizer,
    filter=["lowercase"],
)

edge_ngram_search_analyzer = analyzer(
    'edge_ngram_search_analyzer',
    tokenizer="lowercase",
)



def format_field_for_suggestion(text):
    text_list = text.split(' ')
    l = len(text_list)
    final_text_list = [text_list[x:l] for x in range(l)]
    final_text = [' '.join(x).lower() for x in final_text_list]
    return final_text


class LibraryBaseDocument(object):

    ###################################################################
    # field preparation
    ###################################################################
    def prepare_autocomplete(self, instance):
        raise NotImplementedError('prepare_autocomplete needs to be implemented')

    def prepare_name(self, instance):
        return instance.name.strip()

    def prepare_tags(self, instance):
        return [i.strip() for i in instance.d_tags.split(',') if len(i) > 2]
        #return [i.name for i in instance.tags.all()]

    def prepare_image(self, instance):
        if hasattr(instance, 'main_image') and instance.main_image:
            try:
                return get_thumbnailer(instance.main_image).get_thumbnail(THUMBNAIL_OPT).url
            except InvalidImageFormatError:
                pass


@label_index.doc_type
class LabelDocument(LibraryBaseDocument, DocType):

    class Meta:
        model = Label
        queryset_pagination = 1000
        doc_type = 'alibrary.label'

        fields = [
            'type',
        ]

    autocomplete = fields.TextField(
        analyzer=edge_ngram_analyzer,
        search_analyzer=edge_ngram_search_analyzer,
    )

    url = fields.KeywordField(attr='get_absolute_url')
    api_url = fields.KeywordField(attr='get_api_url')

    name = fields.TextField()
    tags = KeywordField()
    image = KeywordField()



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

        fields = [
            'type',
        ]

    autocomplete = fields.TextField(
        analyzer=edge_ngram_analyzer,
        search_analyzer=edge_ngram_search_analyzer,
    )

    url = fields.KeywordField(attr='get_absolute_url')
    api_url = fields.KeywordField(attr='get_api_url')

    name = fields.TextField()
    tags = KeywordField()
    image = KeywordField()

    year_start = fields.IntegerField()
    year_end = fields.IntegerField()

    description = fields.TextField(attr='biography')
    country = KeywordField(attr='country.iso2_code')


    ###################################################################
    # field preparation
    ###################################################################
    def prepare_autocomplete(self, instance):
        text = [instance.name.strip()]
        return text

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
        return super(ArtistDocument, self).get_queryset().select_related('country')





# @label_index.doc_type
# class LabelDocument(DocType):
#
#     class Meta:
#         model = Label
#         queryset_pagination = 1000
#         doc_type = 'alibrary.label'
#
#         fields = [
#             'type',
#         ]
#
#     autocomplete = fields.TextField(
#         analyzer=edge_ngram_analyzer,
#         search_analyzer=edge_ngram_search_analyzer,
#     )
#
#     name = fields.TextField()
#     tags = KeywordField()
#     url = fields.KeywordField(attr='get_absolute_url')
#     api_url = fields.KeywordField(attr='get_api_url')
#     image = KeywordField()
#     year_start = fields.IntegerField()
#     year_end = fields.IntegerField()
#
#     description = fields.TextField(attr='description')
#     country = KeywordField(attr='country.iso2_code')
#
#
#     ###################################################################
#     # field preparation
#     ###################################################################
#     def prepare_autocomplete(self, instance):
#         text = [instance.name.strip()]
#         # TODO: check what exact fields needed
#         if instance.parent:
#             text += [instance.parent.name.strip()]
#         if instance.get_root():
#             text += [instance.get_root().name.strip()]
#         if instance.country:
#             text += [instance.country.iso2_code]
#
#         return text
#
#     def prepare_name(self, instance):
#         return instance.name.strip()
#
#     def prepare_tags(self, instance):
#         return [i.strip() for i in instance.d_tags.split(',') if len(i) > 2]
#         #return [i.name for i in instance.tags.all()]
#
#     def prepare_image(self, instance):
#         if hasattr(instance, 'main_image') and instance.main_image:
#             try:
#                 return get_thumbnailer(instance.main_image).get_thumbnail(THUMBNAIL_OPT).url
#             except InvalidImageFormatError:
#                 pass
#
#     def prepare_year_start(self, instance):
#         if instance.date_start:
#             return instance.date_start.year
#
#     def prepare_year_end(self, instance):
#         if instance.date_end:
#             return instance.date_end.year
#
#
#     ###################################################################
#     # custom queryset
#     ###################################################################
#     def get_queryset(self):
#         return super(LabelDocument, self).get_queryset().select_related('country', 'parent')
#
