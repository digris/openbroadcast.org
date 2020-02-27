# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from abcast.models import Station
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView
from django.shortcuts import redirect
from django.utils.translation import ugettext as _


class StationListView(ListView):

    queryset = Station.objects.all().order_by('name')
    template_name = "abcast/station/list.html"


class StationDetailView(DetailView):

    model = Station
    template_name = "abcast/station/detail.html"
    section_template_base = "abcast/station/_detail"
    slug_field = "uuid"
    slug_url_kwarg = 'uuid'

    section = None
    sections = [
        ("profile", _("Profile")),
        ("members", _("Members")),
    ]

    def dispatch(self, request, *args, **kwargs):

        # get default section if none provided
        if not kwargs.get("section"):
            redirect_to = reverse(
                "abcast-station-detail", kwargs={"uuid": kwargs.get("uuid"), "section": self.sections[0][0]}
            )
            return redirect(redirect_to)
        else:
            self.section = kwargs.get("section")

        return super(StationDetailView, self).dispatch(request, *args, **kwargs)

    def get_section_menu(self, object, section):
        menu = []
        for key, title in self.sections:

            menu.append(
                {
                    "active": key == section,
                    "title": title,
                    "url": reverse(
                        "abcast-station-detail",
                        kwargs={"uuid": object.uuid, "section": key},
                    ),
                }
            )

        return menu

    def get_section_template(self):
        template = "{base}_{section}.html".format(
            base=self.section_template_base, section=self.section
        )
        return template

    def get_context_data(self, **kwargs):
        context = super(StationDetailView, self).get_context_data(**kwargs)

        section_menu = self.get_section_menu(object=self.object, section=self.section)

        ###############################################################
        # generic context, needed for all sections
        ###############################################################
        context.update(
            {
                "section": self.section,
                "section_menu": section_menu,
                "section_template": self.get_section_template(),
            }
        )

        if self.section == "members":
            obj = self.get_object()
            context.update({
                'members': obj.members.all()
            })

        return context
