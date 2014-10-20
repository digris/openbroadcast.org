from django.contrib.sitemaps import Sitemap
from alibrary.models import Release

class ReleaseSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    
    def items(self):
        return Release.objects.all().order_by('-updated')

    def lastmod(self, obj):
        return obj.updated