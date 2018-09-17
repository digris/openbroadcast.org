# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
elasticsearch index documents
"""
from actstream.models import actor_stream
from django.utils import timezone
from datetime import timedelta
from django_elasticsearch_dsl import DocType, Index, KeywordField, fields
from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.exceptions import InvalidImageFormatError
from search.elasticsearch_utils import edge_ngram_analyzer, edge_ngram_search_analyzer
from .models import Profile

THUMBNAIL_OPT = dict(size=(197, 197), crop=True, upscale=True)

profile_index = Index('profiles')

@profile_index.doc_type
class ProfileDocument(DocType):

    class Meta:
        model = Profile
        queryset_pagination = 1000
        doc_type = 'profiles.profile'

    autocomplete = fields.TextField(
        analyzer=edge_ngram_analyzer,
        search_analyzer=edge_ngram_search_analyzer,
    )

    url = fields.KeywordField(attr='get_absolute_url')
    api_url = fields.KeywordField(attr='get_api_url')
    created = fields.DateField()
    updated = fields.DateField()

    # time/date properties from user model
    date_joined = fields.DateField(attr='user.date_joined')
    last_login = fields.DateField(attr='user.last_login')

    name = fields.TextField(fielddata=True)
    # exact_name = fields.KeywordField(attr='name')
    tags = KeywordField()

    expertise = KeywordField()
    groups = KeywordField()


    # labelcode = KeywordField()
    #
    # # tags = fields.NestedField(properties={
    # #     'name': fields.KeywordField(),
    # #     'id': fields.IntegerField(),
    # # })
    #
    # creator = fields.KeywordField(attr='creator.username')
    #
    #
    image = KeywordField()
    #
    # type = fields.KeywordField(attr='get_type_display')
    #
    # year_start = fields.IntegerField()
    # year_end = fields.IntegerField()
    #
    # description = fields.TextField(attr='description')
    country = KeywordField(attr='country.printable_name')


    # recent_activity = fields.IntegerField()


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
    #
    def prepare_name(self, instance):
        return instance.get_display_name().strip()

    def prepare_tags(self, instance):
        return [i.strip() for i in instance.d_tags.split(',') if len(i) > 2]

    def prepare_groups(self, instance):
        return [g.name.strip() for g in instance.user.groups.all()]

    def prepare_expertise(self, instance):
        return [e.name.strip() for e in instance.expertise.all()]

    def prepare_image(self, instance):
        if hasattr(instance, 'main_image') and instance.main_image:
            try:
                return get_thumbnailer(instance.main_image).get_thumbnail(THUMBNAIL_OPT).url
            except InvalidImageFormatError as e:
                pass

    # def prepare_recent_activity(self, instance):
    #     return actor_stream(instance.user).filter(
    #         timestamp__gte=timezone.now() - timedelta(days=365)
    #     ).count()

    # def prepare_year_start(self, instance):
    #     if instance.date_start:
    #         return instance.date_start.year
    #
    # def prepare_year_end(self, instance):
    #     if instance.date_end:
    #         return instance.date_end.year

    ###################################################################
    # custom queryset
    ###################################################################
    def get_queryset(self):
        return super(ProfileDocument, self).get_queryset().select_related('user', 'mentor')

