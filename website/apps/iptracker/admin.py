# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Host

class HostAdmin(admin.ModelAdmin):

    pass

admin.site.register(Host, HostAdmin)