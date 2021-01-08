# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import DetailView, ListView
from django.shortcuts import redirect
from django.http import Http404


class UUIDDetailView(DetailView):
    slug_field = "uuid"
    slug_url_kwarg = "uuid"


class SectionDetailView(UUIDDetailView, DetailView):

    # model
    # template_name
    url_name = None
    default_section = None
    section_template_pattern = None
    section = None
    section_key = None
    sections = []

    def __init__(self, *args, **kwargs):
        if not self.section_template_pattern:
            raise ImproperlyConfigured('please provide "section_template_pattern"')
        try:
            tpl = self.section_template_pattern.format(key="test")
            assert type(tpl) == unicode
        except (KeyError, IndexError, AttributeError, AssertionError):
            raise ImproperlyConfigured(
                "invalid template pattern: {}".format(self.section_template_pattern)
            )

        super(SectionDetailView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):

        section_url_suffix = kwargs.get("section")

        current_section = next(
            (s for s in self.get_sections() if s["url"] == section_url_suffix), None
        )

        if not current_section:
            raise Http404('invalid section "{}"'.format(section_url_suffix))

        self.section = current_section
        self.section_key = current_section["key"]

        return super(SectionDetailView, self).dispatch(request, *args, **kwargs)

    def get_sections(self):
        return self.sections

    def get_default_section(self):
        if self.default_section:
            return self.default_section

    def get_section_template(self):
        return self.section_template_pattern.format(key=self.section_key)

    def get_section_menu(self, obj, section_key):
        menu = []
        for section in self.get_sections():
            print(section)
            url_kwargs = {
                "uuid": obj.uuid,
            }
            if section.get("url"):
                url_kwargs.update(
                    {
                        "section": section.get("url"),
                    }
                )

            menu.append(
                {
                    "active": section.get("key") == section_key,
                    "title": section.get("title"),
                    "url": reverse(
                        self.url_name,
                        kwargs=url_kwargs,
                    ),
                }
            )
        return menu

    def get_context_data(self, **kwargs):
        context = super(SectionDetailView, self).get_context_data(**kwargs)

        section_menu = self.get_section_menu(
            obj=self.object, section_key=self.section_key
        )

        context.update(
            {
                "section": self.section,
                "section_menu": section_menu,
                "section_template": self.get_section_template(),
            }
        )

        return context
