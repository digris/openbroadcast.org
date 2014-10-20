from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from l10n.models import Country, AdminArea


class AdminArea_Inline(admin.TabularInline):
    model = AdminArea
    extra = 1

class CountryOptions(admin.ModelAdmin):
    
    def make_active(self, request, queryset):
        rows_updated = queryset.update(active=True)
        if rows_updated == 1:
            message_bit = _("1 country was")
        else:
            message_bit = _("%s countries were" % rows_updated)
        self.message_user(request,
                          _("%s successfully marked as active") % message_bit)
    make_active.short_description = _("Mark selected countries as active")
    
    def make_inactive(self, request, queryset):
        rows_updated = queryset.update(active=False)
        if rows_updated == 1:
            message_bit = _("1 country was")
        else:
            message_bit = _("%s countries were" % rows_updated)
        self.message_user(request,
                          _("%s successfully marked as inactive") % message_bit)
    make_inactive.short_description = _("Mark selected countries as inactive")
    
    list_display = ('printable_name', 'iso2_code','active')
    list_filter = ('continent', 'active')
    search_fields = ('name', 'iso2_code', 'iso3_code')
    actions = ('make_active', 'make_inactive')
    inlines = [AdminArea_Inline]

admin.site.register(Country, CountryOptions)

class CountryAreaAdmin(admin.ModelAdmin):
    """
    provides an AJAX-controlled country-area dropdowns
    """
    change_form_template = "l10n/admin/change_form.html"
    country_field = "country"
    area_field = "area"
    area_field_required = "true"

    def get_urls(self):
        urls = super(CountryAreaAdmin, self).get_urls()
        from l10n.urls import urlpatterns
        return urlpatterns + urls

    def extra_context(self, extra_context):
        if extra_context is None:
            extra_context = {}
        extra_context.update({
                'country_field': self.country_field,
                'area_field': self.area_field,
                'area_field_required': self.area_field_required,
                })
        return extra_context

    def add_view(self, *args, **kwargs):
        extra_context = kwargs.get('extra_context', {})
        kwargs['extra_context'] = self.extra_context(extra_context)
        return super(CountryAreaAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        extra_context = kwargs.get('extra_context', {})
        kwargs['extra_context'] = self.extra_context(extra_context)
        return super(CountryAreaAdmin, self).change_view(*args, **kwargs)

    class Media:
        js = ("l10n/js/country.area.js",)
