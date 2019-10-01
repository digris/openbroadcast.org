# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from tagging.models import Tag, TaggedItem
from tagging.forms import TagAdminForm


def merge_tags(modeladmin, request, queryset):
    main = queryset[0]
    slaves = [x for x in queryset[1:]]

    for tag in slaves:
        item_pks = [t.pk for t in tag.items.all()]

        for pk in item_pks:
            try:
                TaggedItem.objects.filter(pk=pk).update(tag=main)
            except Exception as e:
                print(e)

        tag.delete()

    modeladmin.message_user(
        request,
        "%s is merged with other places, now you can give it a canonical name." % main,
    )


merge_tags.short_description = _("Merge selected tags")


class TagMergeForm(forms.Form):
    def __init__(self, queryset, *args, **kwargs):
        super(TagMergeForm, self).__init__(*args, **kwargs)
        self.fields["master"].queryset = queryset

    master = forms.ModelChoiceField(queryset=None, required=True)


class CustomTagAdmin(admin.ModelAdmin):
    form = TagAdminForm

    list_display = ("name", "usage_info", "type", "created", "updated")

    date_hierarchy = "created"

    list_filter = ["type", "created", "updated"]

    search_fields = ("name",)

    list_editable = ["type"]

    actions = [merge_tags]

    def usage_info(self, obj):
        return "{}".format(obj.items.nocache().count())

    usage_info.short_description = _("Usage")
    usage_info.allow_tags = True


admin.site.unregister(Tag)
admin.site.register(Tag, CustomTagAdmin)
