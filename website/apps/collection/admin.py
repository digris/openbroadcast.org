# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from collection.models import Collection, CollectionItem, CollectionMember, CollectionMaintainer

admin.site.register(CollectionItem)
admin.site.register(CollectionMember)

class CollectionItemInline(admin.TabularInline):
    model = CollectionMember
    raw_id_fields = [
        'added_by',
    ]
    extra=0

class CollectionMaintainerInline(admin.TabularInline):
    model = CollectionMaintainer
    raw_id_fields = [
        'user',
    ]
    extra=0


class CollectionAdmin(admin.ModelAdmin):
    inlines = [
        CollectionMaintainerInline,
        CollectionItemInline,
    ]

admin.site.register(Collection, CollectionAdmin)
