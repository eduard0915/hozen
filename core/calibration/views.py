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

from core.calibration.forms import CalibrationForm
from core.calibration.models import Calibration
from core.equipment.models import Equipment
from core.mixins import ValidatePermissionRequiredMixin


# Registro de Calibración
class CalibrationCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Calibration
    form_class = CalibrationForm
    template_name = 'create_calibration.html'
    success_url = reverse_lazy('calibration:list_calibration')
    permission_required = 'calibration.add_calibration'
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
                    messages.success(request, f'Calibración de equipo realizada satisfactoriamente!')
                else:
                    messages.error(request, form.errors)
            else:
                data['error'] = 'No ha ingresado datos en los campos'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipment'] = Equipment.objects.filter(calibration=True)
        context['title'] = 'Registro de Calibración'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['entity'] = 'Registro de Calibración'
        context['div'] = '12'
        return context


# Registros de Calibración
class CalibrationListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Calibration
    template_name = 'list_calibration.html'
    permission_required = 'calibration.view_calibration'

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
                equip = list(Calibration.objects.select_related('equipment').values(
                    'id',
                    'equipment',
                    'equipment__code',
                    'equipment__description',
                    'equipment__serial',
                    'certificate_number',
                    'calibration_certificate',
                    'calibration_made_by',
                    'comments_calibration',
                    'date_calibration',
                    'date_calibration_next',
                ).order_by('-id'))
                return JsonResponse(equip, safe=False)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Calibraciones'
        context['create_url'] = reverse_lazy('calibration:create_calibration')
        context['entity'] = 'Registros de Calibraciones'
        return context


# Edición de Registro de Calibración
class CalibrationUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Calibration
    form_class = CalibrationForm
    template_name = 'create_calibration.html'
    success_url = reverse_lazy('calibration:list_calibration')
    permission_required = 'calibration.change_calibration'
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
                    messages.success(request, f'Registro de calibración editado satisfactoriamente!')
                else:
                    messages.error(request, form.errors)
            else:
                data['error'] = 'No ha ingresado datos en los campos'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['calibration'] = Calibration.objects.get(pk=self.kwargs.get('pk'))
        context['equipment'] = Equipment.objects.filter(calibration=True)
        context['title'] = 'Edición de Registro de Calibración'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['entity'] = 'Edición de Registro de Calibración'
        context['div'] = '12'
        return context


# Detalle mantenimiento desde listado de equipo (descripción y cambio de piezas)
class CalibrationDetailView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DetailView):
    model = Calibration
    template_name = 'detail_calibration_modal.html'
    permission_required = 'calibration.view_calibration'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super(CalibrationDetailView, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        detail = Calibration.objects.get(pk=self.kwargs.get('pk'))
        context['entity'] = 'Observaciones Calibración: ' + detail.equipment.description
        return context


# Descarga Certificado de calibración
class CalibrationCertificateDownloadView(LoginRequiredMixin, ValidatePermissionRequiredMixin, View):
    permission_required = 'calibration.view_calibration'

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
                document = Calibration.objects.get(id=docid)
            except Calibration.DoesNotExist:
                return HttpResponse('El documento solicitado no existe')
            if document is not None:
                if doctype:
                    if doctype == 'calibration_certificate':
                        object_name = 'media/' + str(document.calibration_certificate)
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
                        filename = 'certificado_calibracion_equipo_' + document.equipment.code + '.' + ext
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
