from django.views.generic import TemplateView


class ExporterIndexView(TemplateView):
    template_name = "exporter/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
