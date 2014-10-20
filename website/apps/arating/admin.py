from django.contrib import admin

class BaseAdmin(admin.ModelAdmin):
    save_on_top = True

from arating.models import Vote


class VoteAdmin(BaseAdmin):
    pass

admin.site.register(Vote, VoteAdmin)



