from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, UpdateView, DetailView, FormView

from core.mixins import ValidatePermissionRequiredMixin
from core.user.forms import *
from core.user.models import User, AcademicTraining


# Creación de usuario
class UserCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'create.html'
    success_url = reverse_lazy('user:user_list')
    permission_required = 'user.add_user'
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
                    name_username = form.cleaned_data.get('username')
                    messages.success(request, f'Usuario "{name_username}" creado satisfactoriamente!')
                else:
                    messages.error(request, form.errors)
            else:
                data['error'] = 'No ha ingresado datos en los campos'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['entity'] = 'Creación de Usuario'
        return context


# Listado de usuarios
class UserListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = User
    template_name = 'list_user.html'
    permission_required = 'user.add_user'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                user = list(User.objects.values(
                    'id',
                    'last_login',
                    'cedula',
                    'username',
                    'cargo',
                    'groups__name',
                    'email',
                    'is_active',
                    'first_name',
                    'last_name'
                ).filter(is_superuser=False).order_by('first_name'))
                return JsonResponse(user, safe=False)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Usuarios'
        context['create_url'] = reverse_lazy('user:user_create')
        context['list_url'] = reverse_lazy('user:user_list')
        context['entity'] = 'Usuarios'
        return context


# Edición de usuario por Administrador
class UserUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'create.html'
    success_url = reverse_lazy('user:user_list')
    permission_required = 'user.change_user'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
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
                    name_username = form.cleaned_data.get('username')
                    messages.success(request, f'Usuario "{name_username}" actualizado satisfactoriamente!')
                else:
                    messages.error(request, form.errors)
            else:
                data['error'] = 'No ha ingresado datos en los campos'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de Usuarios'
        context['list_url'] = self.success_url
        context['entity'] = 'Editar Usuario'
        context['action'] = 'edit'
        context['users'] = User.objects.all()
        return context


# Inactivar usuario
class UserInactiveView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserInactiveForm
    template_name = 'active_user.html'
    success_url = reverse_lazy('user:user_list')
    permission_required = 'user.change_user'
    url_redirect = success_url

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.method = None

    @method_decorator(csrf_exempt)
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
                    messages.success(request, f'Usuario inactivado satisfactoriamente!')
                else:
                    messages.error(request, form.errors)
            else:
                data['error'] = 'No ha ingresado datos en los campos'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs.get('pk'))
        context['list_url'] = self.success_url
        context['entity'] = 'Editar Usuario'
        context['action'] = 'edit'
        context['entity'] = 'Está seguro de inactivar el usuario ' + user.get_full_name()
        context['act'] = reverse_lazy('user:user_inactive', kwargs={'pk': user.id})
        return context


# Activar Usuario
class UserActiveView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserActiveForm
    template_name = 'active_user.html'
    success_url = reverse_lazy('user:user_list')
    permission_required = 'user.change_user'
    url_redirect = success_url

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.method = None

    @method_decorator(csrf_exempt)
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
                    messages.success(request, f'Usuario activado satisfactoriamente!')
                else:
                    messages.error(request, form.errors)
            else:
                data['error'] = 'No ha ingresado datos en los campos'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs.get('pk'))
        context['list_url'] = self.success_url
        context['entity'] = 'Editar Usuario'
        context['action'] = 'edit'
        context['entity'] = 'Está seguro de activar el usuario ' + user.get_full_name()
        context['act'] = reverse_lazy('user:user_active', kwargs={'pk': user.id})
        return context


# Detalle de Usuario por administrador
class UserDetailView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DetailView):
    model = User
    template_name = 'detail_user.html'
    permission_required = 'user.change_user'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super(UserDetailView, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['academic'] = AcademicTraining.objects.filter(user_id=self.kwargs.get('pk'))
        context['title'] = 'Perfil de Usuario'
        context['entity'] = 'Perfil de Usuario'
        return context


# Detalle de Perfil de usuario autenticado
class ProfileDetailView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DetailView):
    model = User
    template_name = 'profile_user.html'
    permission_required = 'user.view_user'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super(ProfileDetailView, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['academic'] = AcademicTraining.objects.filter(user=self.kwargs.get('pk'))
        context['title'] = 'Mi Perfil'
        context['entity'] = 'Mi Perfil'
        return context


# Edición de perfil por usuario autenticado
class ProfileUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'create.html'
    success_url = reverse_lazy('inicio:inicio')
    permission_required = 'user.view_user'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        global form
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                if form.is_valid():
                    data = form.save()
                    messages.success(request, f'Su perfil ha sido actualizado satisfactoriamente!')
                else:
                    messages.error(request, form.errors)
            else:
                data['error'] = 'No ha ingresado datos en los campos'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Perfil'
        context['list_url'] = reverse_lazy('user:user_profile', kwargs={'pk': self.kwargs.get('pk')})
        context['entity'] = 'Editar Perfil'
        context['action'] = 'edit'
        return context


# Reseteo de contraseña por administrador
class UserPasswordUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserPasswordUpdateForm
    template_name = 'change_password.html'
    success_url = reverse_lazy('user:user_list')
    permission_required = 'user.change_user'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        global form
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                if form.is_valid():
                    data = form.save()
                    messages.success(request, f'Contraseña de usuario reseteada satisfactoriamente!')
                else:
                    messages.error(request, form.errors)
            else:
                data['error'] = 'No ha ingresado datos en los campos'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs.get('pk'))
        context['title'] = 'Reseteo de Contraseña'
        context['list_url'] = self.success_url
        context['entity'] = 'Reseteo de Contraseña de Usuario'
        context['action'] = 'edit'
        context['act'] = reverse_lazy('user:user_password_update', kwargs={'pk': user.id})
        return context


# Cambio de contraseña por usuario
class UserChangePasswordView(LoginRequiredMixin, ValidatePermissionRequiredMixin, FormView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'change_password.html'
    permission_required = 'user.view_user'
    success_url = reverse_lazy('user:change_password')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = PasswordChangeForm(user=self.request.user)
        form.fields['old_password'].widget.attrs['class'] = 'form-control'
        form.fields['new_password1'].widget.attrs['class'] = 'form-control'
        form.fields['new_password1'].help_text = 'Alfanumérica, mínimo de 8 caracteres, no parecerse a su información ' \
                                                 'personal, ni a otra contraseña utilizada '
        form.fields['new_password2'].widget.attrs['class'] = 'form-control'
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = PasswordChangeForm(user=request.user, data=request.POST)
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, form.user)
                    messages.success(request, f'Su contraseña fue actualizada satisfactoriamente!')
                else:
                    messages.error(request, form.errors)
            else:
                data['error'] = 'No ha ingresado datos en los campos'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = self.success_url
        context['entity'] = 'Actualización de Contraseña'
        context['action'] = 'edit'
        context['act'] = reverse_lazy('user:change_password')
        return context


# Registro de formación académica
class AcademicTrainingCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = AcademicTraining
    form_class = AcademicTrainingForm
    template_name = 'create_academic_modal.html'
    permission_required = 'user.add_user'

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
                else:
                    messages.error(request, form.errors)
            else:
                data['error'] = 'No ha ingresado datos en los campos'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.kwargs.get('pk')})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs.get('pk'))
        context['action'] = 'add'
        context['user'] = user
        context['entity'] = 'Registro de Formación Académica'
        context['act'] = reverse_lazy('user:academic_create', kwargs={'pk': user.id})
        return context


# Edición de Registro de formación académica
class AcademicTrainingUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = AcademicTraining
    form_class = AcademicTrainingUpdateForm
    template_name = 'create_academic_modal.html'
    permission_required = 'user.change_user'

    @method_decorator(csrf_exempt)
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
                else:
                    messages.error(request, form.errors)
            else:
                data['error'] = 'No ha ingresado datos en los campos'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = AcademicTraining.objects.get(pk=self.kwargs.get('pk'))
        context['action'] = 'edit'
        context['entity'] = 'Edición de Registro de Formación Académica'
        context['act'] = reverse_lazy('user:academic_update', kwargs={'pk': user.id})
        return context
