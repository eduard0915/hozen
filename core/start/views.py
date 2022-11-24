from django.views.generic import TemplateView


class StartView(TemplateView):
    template_name = 'start.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Inicio'
        return context


class NotPermsView(TemplateView):
    template_name = 'not_perms.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sin Permisos de Acceso'
        return context
