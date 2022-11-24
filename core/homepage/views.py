from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Hozen Manager'
        return context


class NotPermsView(TemplateView):
    template_name = 'not_perms.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sin Permisos de Acceso'
        return context
