from django.contrib import admin
from tagging.models import Tag, TaggedItem
from tagging.forms import TagAdminForm
from tagging.utils import merge
from django.contrib.admin import helpers
from django.template.response import TemplateResponse

def merge_tags(modeladmin, request, queryset):


    if request.POST.get('master_tag'):
        print 'POST!!!!!!!!!!'
        master_tag = Tag.objects.get(pk=int(request.POST.get('master_tag')))
        tag_ids = request.POST.get('tag_ids').split(',')

        for t in Tag.objects.exclude(pk=master_tag.pk).filter(pk__in=tag_ids):
            print 'slave: %s' % t
            for i in t.items.all():
                merge(master_tag, t)
    else:
        context = {
            'title': "Are you sure?",
            'queryset': queryset,
            'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
        }
        return TemplateResponse(request, 'admin/confirm_merge.html',
            context, current_app=modeladmin.admin_site.name)








merge_tags.short_description = "Merge selected tags"


class TagAdmin(admin.ModelAdmin):

    form = TagAdminForm
    list_display = ['name', 'usage_count', ]
    search_fields = ('name',)
    actions = [merge_tags,]

    def usage_count(self, obj):
        return '%s' % obj.items.count()
    usage_count.short_description = 'Usage'


admin.site.register(TaggedItem)
admin.site.register(Tag, TagAdmin)



