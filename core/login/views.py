from django.contrib.auth.views import *
from django.shortcuts import redirect
from django.urls import reverse_lazy

from config import settings


# Login para iniciar sesión
class LoginFormView(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesión'
        return context


# Solicitud de reseteo de contraseña
class FormResetPasswordView(PasswordResetView):
    template_name = 'reset_password_form.html'
    email_template_name = 'reset_password_email.html'
    success_url = reverse_lazy('password_reset_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Recuperar contraseña'
        return context


# Completitud de la solicitud de reseteo de contraseña
class ResetPasswordDoneView(PasswordResetDoneView):
    template_name = 'reset_password_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contraseña enviada'
        return context


# Registro de contraseña
class ResetConfirmPasswordView(PasswordResetConfirmView):
    template_name = 'reset_password_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cambiar contraseña'
        return context


# Finalización de cambio de contraseña
class ResetCompletePasswordView(PasswordResetCompleteView):
    template_name = 'reset_password_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contraseña actualizada'
        return context
