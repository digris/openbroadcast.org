# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView
from django.shortcuts import redirect


class UUIDDetailView(DetailView):
    slug_field = "uuid"
    slug_url_kwarg = 'uuid'


# class SectionDetailView(DetailView):
#
#     url_name = None
#     section = None
#     default_section = None
#     section_template_prefix = None
#     sections = []
#
#     def get_default_section(self):
#         if self.default_section:
#             return self.default_section
#
#
#     def get_section_menu(self, ob, current_section):
#         menu = []
#         for key, title in self.sections:
#             menu.append(
#                 {
#                     "active": key == current_section,
#                     "title": title,
#                     "url": reverse(
#                         self.url_name,
#                         kwargs={"uuid": ob.uuid, "section": key},
#                     ),
#                 }
#             )
#         return menu
