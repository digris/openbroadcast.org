from django.contrib import admin
from .models import Documentation

@admin.register(Documentation)
class DocumentationAdmin(admin.ModelAdmin):
    pass