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
                TaggedItem.objects.filter(
                    pk=pk
                ).update(tag=main)
            except Exception as e:
                print(e)

        tag.delete()

    modeladmin.message_user(request, "%s is merged with other places, now you can give it a canonical name." % main)


merge_tags.short_description = _('Merge selected tags')

class TagMergeForm(forms.Form):

    def __init__(self, queryset, *args, **kwargs):
        super(TagMergeForm, self).__init__(*args, **kwargs)
        self.fields['master'].queryset = queryset

    master = forms.ModelChoiceField(queryset=None, required=True)

    #master = forms.ModelChoiceField(queryset=Tag.objects.all()[0:10])

# class CustomTagAdmin(admin.ModelAdmin):
#
#     form = TagAdminForm
#
#     list_display = ('name', 'usage_info')
#
#     search_fields = ('name',)
#
#     actions = [
#         'merge_tags',
#     ]
#
#     def usage_info(self, obj):
#         return '{}'.format(obj.items.count())
#
#     usage_info.short_description = _('Usage')
#     usage_info.allow_tags = True
#
#
#     def merge_tags(self, request, queryset):
#
#         print '--**--**--**--**--**'
#
#         if 'do_action' in request.POST:
#             form = TagMergeForm(request.POST)
#             if form.is_valid():
#                 master = form.cleaned_data['master']
#                 print '******************************'
#                 print master
#                 return
#         else:
#             form = TagMergeForm(queryset=queryset)
#
#         return render(request, 'admin/tagging/merge_form.html',
#                       {'title': u'Choose Master Tag',
#                        'objects': queryset,
#                        'form': form})
#
#
#     merge_tags.short_description = _('Merge selected tags')




class CustomTagAdmin(admin.ModelAdmin):
    form = TagAdminForm

    list_display = ('name', 'usage_info')

    search_fields = ('name',)

    actions = [
        merge_tags,
    ]

    def usage_info(self, obj):
        return '{}'.format(obj.items.nocache().count())

    usage_info.short_description = _('Usage')
    usage_info.allow_tags = True


admin.site.unregister(Tag)
admin.site.register(Tag, CustomTagAdmin)
