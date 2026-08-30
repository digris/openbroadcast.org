from django.views.generic import TemplateView
from navutils import MenuMixin


class ExporterIndexView(MenuMixin, TemplateView):
    template_name = "exporter/index.html"
    current_menu_item = "data:exporter"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
