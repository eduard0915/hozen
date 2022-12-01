from django.forms import *

from core.user.models import User


# Creación de usuario
class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['groups'].label = 'Perfil'
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name', 'email',
            'cargo', 'cellphone',
            'cedula', 'username',
            'password', 'groups',
            'is_active'
        ]
        widgets = {
            'password': PasswordInput(render_value=True, attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name': TextInput(attrs={'class': 'form-control', 'required': True}),
            'email': EmailInput(attrs={'class': 'form-control', 'required': True}),
            'cargo': TextInput(attrs={'class': 'form-control'}),
            'cellphone': TextInput(attrs={'class': 'form-control'}),
            'cedula': TextInput(attrs={'class': 'form-control'}),
            'username': TextInput(attrs={'class': 'form-control'}),
            'groups': SelectMultiple(attrs={'class': 'form-control', 'required': True})
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_staff', 'is_active']
        help_texts = {
            'groups': 'Seleccione perfil del usuario',
            'is_active': 'Indica si el usuario está habilitado',
            'username': 'Únicamente letras y/o números'
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
                u.groups.clear()
                for g in self.cleaned_data['groups']:
                    u.groups.add(g)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


# Edición de usuario por administrador
class UserUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['groups'].label = 'Perfil'
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name', 'email',
            'cargo', 'cellphone',
            'cedula', 'username',
            'groups',
            'is_active',
        ]
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name': TextInput(attrs={'class': 'form-control', 'required': True}),
            'email': EmailInput(attrs={'class': 'form-control', 'required': True}),
            'cargo': TextInput(attrs={'class': 'form-control'}),
            'cellphone': TextInput(attrs={'class': 'form-control'}),
            'cedula': TextInput(attrs={'class': 'form-control'}),
            'username': TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'is_active': NullBooleanSelect(attrs={'class': 'form-control'}),
            'groups': SelectMultiple(attrs={'class': 'form-control', 'required': True}),
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_staff']

        help_texts = {
            'groups': 'Seleccione perfil del usuario',
            'is_active': 'Indica si el usuario está habilitado',
            'username': ''
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                data = form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


# Edición de perfil por usuario logueado
class ProfileUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'cargo',
            'cellphone',
            'cedula',
            'email_person',
        ]
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name': TextInput(attrs={'class': 'form-control', 'required': True}),
            'email': EmailInput(attrs={'class': 'form-control', 'required': True}),
            'email_person': EmailInput(attrs={'class': 'form-control'}),
            'cargo': TextInput(attrs={'class': 'form-control'}),
            'cellphone': TextInput(attrs={'class': 'form-control'}),
            'cedula': TextInput(attrs={'class': 'form-control'}),
        }
        exclude = [
            'user_permissions',
            'last_login',
            'date_joined',
            'is_superuser',
            'is_staff',
            'groups',
            'is_active',
            'username',
            'password'
        ]

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


# Reseteo de contraseña de usuario por administrador
class UserPasswordUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = User
        fields = 'password',
        widgets = {
            'password': PasswordInput(render_value=False, attrs={'class': 'form-control'}),
        }
        help_texts = {
            'password': 'Reseteo de contraseña de usuario'
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
