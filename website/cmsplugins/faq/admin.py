from django.contrib import admin
from models import FAQ, FAQCateqory

class FAQAdmin(admin.ModelAdmin):
    
    list_display = ['question', 'get_answer', 'category', 'lang', 'weight',]
    list_filter = ['category', 'lang']

    save_on_top = True

    def get_answer(self, obj):
        return '%s...' % (obj.answer[0:50])
    get_answer.short_description = 'Answer'


    """
    fieldsets = [
        (None,               {'fields': ['name', 'slug', 'folder']}),
        ('Relations', {'fields': ['parent'], 'classes': ['']}),
        ('Other content', {'fields': ['first_placeholder'], 'classes': ['plugin-holder', 'plugin-holder-nopage']}),
    ]
    """


class FAQInline(admin.StackedInline):

    model = FAQ
    extra = 0
    exclude = ['lang',]



class FAQCateqoryAdmin(admin.ModelAdmin):

    list_display = ['name', 'lang', ]
    list_filter = ['lang']

    save_on_top = True

    inlines = [FAQInline,]


admin.site.register(FAQ, FAQAdmin)
admin.site.register(FAQCateqory, FAQCateqoryAdmin)

