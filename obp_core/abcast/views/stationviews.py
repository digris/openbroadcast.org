from abcast.models import Station
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from navutils import MenuMixin


class StationListView(MenuMixin, ListView):
    queryset = Station.objects.all().order_by("name")
    template_name = "abcast/station/list.html"
    current_menu_item = "network:station-list"


class StationDetailView(MenuMixin, DetailView):
    model = Station
    template_name = "abcast/station/detail.html"
    section_template_base = "abcast/station/_detail"
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
    current_menu_item = "network:station-list"

    section = None
    sections = [
        ("profile", _("Profile")),
        ("members", _("Members")),
    ]

    def dispatch(self, request, *args, **kwargs):

        # get default section if none provided
        if not kwargs.get("section"):
            redirect_to = reverse(
                "abcast-network:station-detail",
                kwargs={"uuid": kwargs.get("uuid"), "section": self.sections[0][0]},
            )
            return redirect(redirect_to)
        else:
            self.section = kwargs.get("section")

        return super().dispatch(request, *args, **kwargs)

    def get_section_menu(self, object, section):
        menu = []
        for key, title in self.sections:
            menu.append(
                {
                    "active": key == section,
                    "title": title,
                    "url": reverse(
                        "abcast-network:station-detail",
                        kwargs={"uuid": object.uuid, "section": key},
                    ),
                }
            )

        return menu

    def get_section_template(self):
        template = f"{self.section_template_base}_{self.section}.html"
        return template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

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
            context.update({"members": obj.members.all()})

        return context
