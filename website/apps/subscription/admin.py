# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from hvad.admin import TranslatableAdmin
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields import TextField
from models import Subscription, Newsletter

@admin.register(Newsletter)
class NewsletterAdmin(TranslatableAdmin):

    list_display = ['__unicode__', 'backend',]
    save_on_top = True

    formfield_overrides = {
        TextField: {'widget': forms.Textarea(attrs={'rows':3, 'cols':32}) },
    }


    def get_fieldsets(self, request, obj=None):
        return (
            (None, {
                'fields':
                    (
                        'name',
                        'title',
                        'description',
                        #'site',
                    ),
            }),

            ("Backend", {
                'fields': (
                    'backend',
                    'backend_id',
                    'backend_api_key',
                ),
            }),
        )


class ActiveSubscriptionFilter(admin.SimpleListFilter):

    title = _('Active Subscriptions')
    parameter_name = 'active'

    def lookups(self, request, model_admin):
        return (
            ('active', u'%s' % (_('Active'))),
            ('canceled', u'%s' % (_('Canceled'))),
        )

    def queryset(self, request, queryset):

        if self.value() == 'active':
            return queryset.filter(opted_out__isnull=True)

        if self.value() == 'canceled':
            return queryset.filter(opted_out__isnull=False)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):

    list_display = ['__unicode__', 'name', 'newsletter', 'channel', 'created', 'confirmed', 'opted_out', 'active_display']
    date_hierarchy = 'created'
    list_filter = [ActiveSubscriptionFilter, 'newsletter', 'channel']
    #readonly_fields = ['status', 'folder',]
    save_on_top = True
    raw_id_fields = ['user', ]

    def active_display(self, obj):
        return obj.opted_out is None

    active_display.short_description = 'Active'
    active_display.boolean = True


