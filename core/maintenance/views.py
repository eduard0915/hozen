from urllib.request import urlopen

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from decouple import config
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, UpdateView, DetailView

from core.equipment.models import Equipment
from core.maintenance.forms import MaintenanceForm, MaintenanceUpdateForm
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

    @staticmethod
    def post(request, *args, **kwargs):
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


# Edición de Registro de Mantenimiento
class MaintenanceUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Maintenance
    form_class = MaintenanceUpdateForm
    template_name = 'create_maintenance.html'
    success_url = reverse_lazy('maintenance:list_maintenance')
    permission_required = 'equipment.change_equipment'
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
                    messages.success(request, f'Registro de mantenimiento editado satisfactoriamente!')
                else:
                    messages.error(request, form.errors)
            else:
                data['error'] = 'No ha ingresado datos en los campos'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['maintenance'] = Maintenance.objects.get(pk=self.kwargs.get('pk'))
        context['equipment'] = Equipment.objects.all()
        context['users'] = User.objects.all()
        context['title'] = 'Edición de Registro de Mantenimiento'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['entity'] = 'Edición de Registro de Mantenimiento'
        context['div'] = '12'
        return context


# Detalle de registro de mantenimiento
class MaintenanceDetailView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DetailView):
    model = Maintenance
    template_name = 'detail_maintenance.html'
    permission_required = 'equipment.view_equipment'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super(MaintenanceDetailView, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        detail = Maintenance.objects.get(pk=self.kwargs.get('pk'))
        context['title'] = 'Mantenimiento ' + detail.maintenance_number
        context['entity'] = 'Registro de Mantenimiento ' + detail.maintenance_number
        context['list_url'] = reverse_lazy('maintenance:list_maintenance')
        return context


# Descarga de Registro Físico
class PhysicalRecordDownloadView(LoginRequiredMixin, ValidatePermissionRequiredMixin, View):
    permission_required = 'equipment.view_equipment'

    @staticmethod
    def get(request):
        s3 = boto3.client(
            's3',
            aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
            config=Config(signature_version='s3v4', region_name=config('REGION_NAME')))
        docid = request.GET.get('id')
        doctype = request.GET.get('type')
        if docid and doctype:
            try:
                document = Maintenance.objects.get(id=docid)
            except Maintenance.DoesNotExist:
                return HttpResponse('El documento solicitado no existe')
            if document is not None:
                if doctype:
                    if doctype == 'physical_record':
                        object_name = 'media/' + str(document.physical_record)
                    else:
                        return HttpResponse('El documento solicitado no existe para el tipo de archivo')
                    try:
                        link = s3.generate_presigned_url(
                            'get_object',
                            Params={'Bucket': config('BUCKET'), 'Key': object_name},
                            ExpiresIn=8000
                        )
                        ext = object_name.split(".")[1]
                        url = urlopen(link)
                        doc = url.read()
                        disposition = 'attachment'
                        filename = 'registro_fisico_' + document.maintenance_number + '.' + ext
                        filename = filename.replace(" ", "_")
                        if ext == 'pdf':
                            disposition = 'inline'
                        response = HttpResponse(doc, content_type="application/" + str(ext))
                        response['Content-Disposition'] = str(disposition) + '; filename=' + filename
                        return response
                    except ClientError as e:
                        return HttpResponse(e)
            else:
                return HttpResponse('El documento solicitado no existe')
        else:
            return HttpResponse('La solicitud es incorrecta, faltan parámetros')
