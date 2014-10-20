from django.contrib import admin
from shortcutter.models import *

class ShortcutCollectionInline(admin.StackedInline):
    model = Shortcut

class ShortcutAdmin(admin.ModelAdmin):    
    
    list_display = ('name',)


class ShortcutCollectionAdmin(admin.ModelAdmin):    
    
    list_display = ('name',)
    
    inlines = (ShortcutCollectionInline,)


admin.site.register(Shortcut, ShortcutAdmin)
admin.site.register(ShortcutCollection, ShortcutCollectionAdmin)

