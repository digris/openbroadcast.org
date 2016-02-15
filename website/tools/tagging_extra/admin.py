# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from tagging.models import Tag, TaggedItem
from tagging.forms import TagAdminForm


def merge_tags(modeladmin, request, queryset):

    main = queryset[0]
    slaves = [x for x in queryset[1:]]

    for tag in slaves:

        try:
            TaggedItem.objects.filter(
                    pk__in=[t.pk for t in tag.items.all()]
            ).update(tag=main)
        except:
            pass
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
