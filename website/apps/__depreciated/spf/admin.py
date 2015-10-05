"""Admin classes for the ``object_events`` app."""
from django.contrib import admin

from .models import Request, Match
# from lib.admin.actions import export_as_csv_action




class MatchAdmin(admin.ModelAdmin):
    list_display = ['status', 'mb_id','title', 'artist','artist_credits', 'artist_credits_secondary','release_list', 'duration', 'isrc_list', 'iswc_list', 'request',]
    list_filter = ['status', ]

class MatchInline(admin.TabularInline):
    model = Match


class RequestAdmin(admin.ModelAdmin):
    list_display = ['swp_id', 'status', 'title', 'recording_datex', 'recording_country','duration', 'rome_protected', 'main_artist', 'publication_datex', 'composer', 'label', 'catalognumber', 'isrc', 'num_results', 'level', 'obp_legacy_id']
    list_filter = ['level', 'num_results', 'status', ]
    inlines = [MatchInline,]


admin.site.register(Request, RequestAdmin)
admin.site.register(Match, MatchAdmin)