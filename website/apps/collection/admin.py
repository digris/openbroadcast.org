# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from collection.models import (
    Collection,
    CollectionItem,
    CollectionMember,
    CollectionMaintainer,
)

admin.site.register(CollectionItem)


@admin.register(CollectionMember)
class CollectionMemberAdmin(admin.ModelAdmin):

    list_display = ["item", "collection", "added_by"]


class CollectionItemInline(admin.TabularInline):
    model = CollectionMember
    raw_id_fields = ["added_by"]
    readonly_fields = ["item"]
    extra = 0


class CollectionMaintainerInline(admin.TabularInline):
    model = CollectionMaintainer
    raw_id_fields = ["user"]
    extra = 0


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):

    list_display = ["name", "owner", "visibility"]

    raw_id_fields = ["owner"]

    inlines = [CollectionMaintainerInline, CollectionItemInline]
