from django.contrib import admin
from collection.models import Collection, CollectionItem, CollectionMember

admin.site.register(CollectionItem)
admin.site.register(CollectionMember)

class CollectionItemInline(admin.TabularInline):
    model = CollectionMember
    #raw_id_fields = ['item',]
    extra=0


class CollectionAdmin(admin.ModelAdmin):
    inlines = [CollectionItemInline]

admin.site.register(Collection, CollectionAdmin)
