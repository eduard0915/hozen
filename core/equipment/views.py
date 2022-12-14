from datetime import date
from urllib.request import urlopen

import boto3 as boto3
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
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from core.equipment.forms import EquipmentForm
from core.equipment.models import Equipment
from core.mixins import ValidatePermissionRequiredMixin


# Registro de equipo
class EquipmentCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'create_equipment.html'
    success_url = reverse_lazy('equipment:list_equipment')
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
        context['title'] = 'Registro de Equipo'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['entity'] = 'Registro de Equipo'
        context['div'] = '12'
        return context


# Listado de Equipos
class EquipmentListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Equipment
    template_name = 'list_equipment.html'
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
                equip = list(Equipment.objects.values(
                    'id',
                    'code',
                    'description',
                    'serial',
                    'fix_active',
                    'status',
                    'maker'
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


# Edici??n de Registro de equipo
class EquipmentUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'create_equipment.html'
    success_url = reverse_lazy('equipment:list_equipment')
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
        context['title'] = 'Edici??n de Equipo'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['entity'] = 'Edici??n de Registro de Equipo'
        context['div'] = '12'
        return context


# Detalle de Equipo
class EquipmentDetailView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DetailView):
    model = Equipment
    template_name = 'detail_equipment.html'
    permission_required = 'equipment.view_equipment'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super(EquipmentDetailView, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        detail = Equipment.objects.get(pk=self.kwargs.get('pk'))
        context['title'] = 'Hoja de Vida: ' + detail.code
        context['entity'] = 'Hoja de Vida: ' + detail.code + ' ' + detail.description
        context['list_url'] = reverse_lazy('equipment:list_equipment')
        context['div'] = '12'
        return context


# Descarga de Manual de Fabricante
class ManufacturerManualDownloadView(LoginRequiredMixin, ValidatePermissionRequiredMixin, View):
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
                document = Equipment.objects.get(id=docid)
            except Equipment.DoesNotExist:
                return HttpResponse('El documento solicitado no existe')
            if document is not None:
                if doctype:
                    if doctype == 'manufacturer_manual':
                        object_name = 'media/' + str(document.manufacturer_manual)
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
                        filename = 'manual_fabricante_' + document.code + '.' + ext
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
            return HttpResponse('La solicitud es incorrecta, faltan par??metros')


# Descarga de Documentos anexos fabricante
class ManufacturerDocsDownloadView(LoginRequiredMixin, ValidatePermissionRequiredMixin, View):
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
                document = Equipment.objects.get(id=docid)
            except Equipment.DoesNotExist:
                return HttpResponse('El documento solicitado no existe')
            if document is not None:
                if doctype:
                    if doctype == 'manufacturer_docs':
                        object_name = 'media/' + str(document.manufacturer_docs)
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
                        filename = 'documento_anexo_fabricante_' + document.code + '.' + ext
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
            return HttpResponse('La solicitud es incorrecta, faltan par??metros')
