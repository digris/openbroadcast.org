from django.contrib import admin
from arating.models import Vote


class BaseAdmin(admin.ModelAdmin):
    save_on_top = True


class VoteAdmin(BaseAdmin):
    pass


admin.site.register(Vote, VoteAdmin)
