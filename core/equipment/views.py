from django.contrib import messages
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from core.equipment.forms import EquipmentForm
from core.equipment.models import Equipment


# Registro de equipo
class EquipmentCreateView(CreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'create_equipment.html'
    success_url = reverse_lazy('equipment:list_equipment')
    # permission_required = 'materials.add_suppliermaterial'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                if form.is_valid():
                    form.save()
                    messages.success(request, f'Equipo creado satisfactoriamente!')
                else:
                    messages.error(request, form.errors)
            else:
                data['error'] = 'No ha ingresado datos en los campos'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de Equipo'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['entity'] = 'Registro de Equipo'
        context['div'] = '12'
        return context


# Listado de Proveedores
class EquipmentListView(ListView):
    model = Equipment
    template_name = 'list_equipment.html'
    # permission_required = 'materials.view_suppliermaterial'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                equip = list(Equipment.objects.values(
                    'id',
                    'code',
                    'description',
                    'serial',
                    'fix_active',
                    'status',
                ).order_by('-id'))
                return JsonResponse(equip, safe=False)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Equipos'
        context['create_url'] = reverse_lazy('equipment:create_equipment')
        context['entity'] = 'Listado de Equipos'
        return context


# Edición de Registro de equipo
class EquipmentUpdateView(UpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'create_equipment.html'
    success_url = reverse_lazy('equipment:list_equipment')
    # permission_required = 'materials.add_suppliermaterial'
    url_redirect = success_url

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.method = None

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                if form.is_valid():
                    form.save()
                    messages.success(request, f'Equipo editado satisfactoriamente!')
                else:
                    messages.error(request, form.errors)
            else:
                data['error'] = 'No ha ingresado datos en los campos'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de Equipo'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['entity'] = 'Edición de Registro de Equipo'
        context['div'] = '12'
        return context
