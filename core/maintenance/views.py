from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView

from core.equipment.models import Equipment
from core.maintenance.forms import MaintenanceForm
from core.maintenance.models import Maintenance
from core.mixins import ValidatePermissionRequiredMixin
from core.user.models import User


# Registro de mantenimiento
class MaintenanceCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'create_maintenance.html'
    success_url = reverse_lazy('maintenance:list_maintenance')
    permission_required = 'equipment.add_equipment'
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
        context['equipment'] = Equipment.objects.all()
        context['users'] = User.objects.all()
        context['title'] = 'Registro de Mantenimiento'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['entity'] = 'Registro de Mantenimiento'
        context['div'] = '12'
        return context


# Listado de Mantenimientos
class MaintenanceListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Maintenance
    template_name = 'list_maintenance.html'
    permission_required = 'equipment.view_equipment'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                equip = list(Maintenance.objects.select_related('equipment', 'made_by').values(
                    'id',
                    'maintenance_number',
                    'maintenance_type',
                    'date_maintenance',
                    'equipment',
                    'equipment__code',
                    'equipment__description',
                    'equipment__serial',
                    'made_by',
                    'made_by__first_name',
                    'made_by__last_name',
                    'made_by__cargo',
                    'contractor',
                ).order_by('-id'))
                return JsonResponse(equip, safe=False)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mantenimientos'
        context['create_url'] = reverse_lazy('maintenance:create_maintenance')
        context['entity'] = 'Registros de Mantenimientos'
        return context
#
#
# # Edición de Registro de equipo
# class EquipmentUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
#     model = Equipment
#     form_class = EquipmentForm
#     template_name = 'create_equipment.html'
#     success_url = reverse_lazy('equipment:list_equipment')
#     permission_required = 'equipment.change_equipment'
#     url_redirect = success_url
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.method = None
#
#     def dispatch(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return super().dispatch(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             action = request.POST['action']
#             if action == 'edit':
#                 form = self.get_form()
#                 if form.is_valid():
#                     form.save()
#                     messages.success(request, f'Equipo editado satisfactoriamente!')
#                 else:
#                     messages.error(request, form.errors)
#             else:
#                 data['error'] = 'No ha ingresado datos en los campos'
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Edición de Equipo'
#         context['list_url'] = self.success_url
#         context['action'] = 'edit'
#         context['entity'] = 'Edición de Registro de Equipo'
#         context['div'] = '12'
#         return context
#
#
# # Detalle de Equipo
# class EquipmentDetailView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DetailView):
#     model = Equipment
#     template_name = 'detail_equipment.html'
#     permission_required = 'equipment.view_equipment'
#
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#
#     def get_queryset(self):
#         return super(EquipmentDetailView, self).get_queryset()
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         detail = Equipment.objects.get(pk=self.kwargs.get('pk'))
#         context['title'] = 'Hoja de Vida: ' + detail.code
#         context['entity'] = 'Hoja de Vida: ' + detail.code + ' ' + detail.description
#         context['list_url'] = reverse_lazy('equipment:list_equipment')
#         context['div'] = '12'
#         return context