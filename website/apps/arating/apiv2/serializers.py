# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db.models import Avg
from rest_framework import serializers


class ObjectRatingSerializer(serializers.Serializer):

    user = None

    def __init__(self, **kwargs):
        self.user = kwargs.pop("user", None)
        super(ObjectRatingSerializer, self).__init__(**kwargs)

    ct = serializers.CharField(read_only=True, source="get_ct")
    uuid = serializers.UUIDField(read_only=True)
    upvotes = serializers.SerializerMethodField()
    downvotes = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()
    avg_vote = serializers.SerializerMethodField()

    def get_upvotes(self, obj):
        return obj.votes.filter(vote__gt=0).count()

    def get_downvotes(self, obj):
        return obj.votes.filter(vote__lt=0).count()

    def get_user_vote(self, obj):
        if not self.user:
            return
        vote_qs = obj.votes.filter(user=self.user)
        if vote_qs.exists():
            return vote_qs.first().vote

    def get_avg_vote(self, obj):
        return obj.votes.aggregate(Avg("vote")).values()[0]
