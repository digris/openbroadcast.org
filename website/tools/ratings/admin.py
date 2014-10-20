from django.contrib import admin

from ratings import models

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'key', 'average', 'total', 'num_votes')
    list_filter = ('content_type',)
    ordering = ('-average', '-num_votes')
    search_fields = ('key',)
    readonly_fields = ('average', 'total', 'num_votes')
    
admin.site.register(models.Score, ScoreAdmin)


class VoteAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'key', 'user', 'score', 
        'created_at', 'modified_at')
    list_filter = ('content_type', 'created_at', 'modified_at')
    ordering = ('-modified_at',)
    search_fields = ('user', 'key')
    readonly_fields = ('user',)

admin.site.register(models.Vote, VoteAdmin)
