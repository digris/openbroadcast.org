# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from actstream import feeds
from actstream import views

urlpatterns = [
    # Syndication Feeds
    url(
        r"^feed/(?P<content_type_id>\d+)/(?P<object_id>\d+)/atom/$",
        feeds.AtomObjectActivityFeed(),
        name="actstream_object_feed_atom",
    ),
    url(
        r"^feed/(?P<content_type_id>\d+)/(?P<object_id>\d+)/$",
        feeds.ObjectActivityFeed(),
        name="actstream_object_feed",
    ),
    url(
        r"^feed/(?P<content_type_id>\d+)/atom/$",
        feeds.AtomModelActivityFeed(),
        name="actstream_model_feed_atom",
    ),
    url(
        r"^feed/(?P<content_type_id>\d+)/(?P<object_id>\d+)/as/$",
        feeds.ActivityStreamsObjectActivityFeed(),
        name="actstream_object_feed_as",
    ),
    url(
        r"^feed/(?P<content_type_id>\d+)/$",
        feeds.ModelActivityFeed(),
        name="actstream_model_feed",
    ),
    url(r"^feed/$", feeds.UserActivityFeed(), name="actstream_feed"),
    url(r"^feed/atom/$", feeds.AtomUserActivityFeed(), name="actstream_feed_atom"),
    # Follow/Unfollow API
    url(
        r"^follow/(?P<content_type_id>\d+)/(?P<object_id>\d+)/$",
        views.follow_unfollow,
        name="actstream_follow",
    ),
    url(
        r"^follow_all/(?P<content_type_id>\d+)/(?P<object_id>\d+)/$",
        views.follow_unfollow,
        {"actor_only": False},
        name="actstream_follow_all",
    ),
    url(
        r"^unfollow/(?P<content_type_id>\d+)/(?P<object_id>\d+)/$",
        views.follow_unfollow,
        {"do_follow": False},
        name="actstream_unfollow",
    ),
    # Follower and Actor lists
    url(
        r"^followers/(?P<content_type_id>\d+)/(?P<object_id>\d+)/$",
        views.followers,
        name="actstream_followers",
    ),
    url(
        r"^actors/(?P<content_type_id>\d+)/(?P<object_id>\d+)/$",
        views.actor,
        name="actstream_actor",
    ),
    url(r"^actors/(?P<content_type_id>\d+)/$", views.model, name="actstream_model"),
    url(r"^detail/(?P<action_id>\d+)/$", views.detail, name="actstream_detail"),
    url(r"^(?P<username>[-\w]+)/$", views.user, name="actstream_user"),
    url(r"^stream/$", views.stream, name="actstream"),
]
