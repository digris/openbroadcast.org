from django.contrib import admin
from models import Step, Guide

class StepAdmin(admin.ModelAdmin):
    
    list_display = ['name', 'guide', 'position',]
    list_filter = ['guide',]

    save_on_top = True

    #def get_answer(self, obj):
    #    return '%s...' % (obj.answer[0:50])
    #get_answer.short_description = 'Answer'


    """
    fieldsets = [
        (None,               {'fields': ['name', 'slug', 'folder']}),
        ('Relations', {'fields': ['parent'], 'classes': ['']}),
        ('Other content', {'fields': ['first_placeholder'], 'classes': ['plugin-holder', 'plugin-holder-nopage']}),
    ]
    """


class StepInline(admin.StackedInline):

    model = Step
    extra = 0
    #exclude = ['lang',]



class GuideAdmin(admin.ModelAdmin):

    list_display = ['name',]

    save_on_top = True

    inlines = [StepInline,]


admin.site.register(Step, StepAdmin)
admin.site.register(Guide, GuideAdmin)

