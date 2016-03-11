# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from tagging.models import Tag, TaggedItem
from tagging.forms import TagAdminForm


def merge_tags(modeladmin, request, queryset):

    main = queryset[0]
    slaves = [x for x in queryset[1:]]

    print '---------------'
    print main
    print slaves


    for tag in slaves:
        print ' - %s' % tag

        item_pks = [t.pk for t in tag.items.all()]
        print item_pks

        for pk in item_pks:
            try:
                TaggedItem.objects.filter(
                        pk=pk
                ).update(tag=main)
            except Exception as e:
                print e

        tag.delete()

    modeladmin.message_user(request, "%s is merged with other places, now you can give it a canonical name." % main)

merge_tags.short_description = _('Merge selected tags')


class CustomTagAdmin(admin.ModelAdmin):
    form = TagAdminForm

    list_display = ('name', 'usage_info')

    search_fields = ('name',)

    actions = [
        merge_tags,
    ]

    def usage_info(self, obj):
        return '{}'.format(obj.items.count())

    usage_info.short_description = _('Usage')
    usage_info.allow_tags = True




    #readonly_fields = ('image_preview',)



admin.site.unregister(Tag)
admin.site.register(Tag, CustomTagAdmin)
