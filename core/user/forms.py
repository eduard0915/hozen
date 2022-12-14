from django.forms import *

from core.user.models import User, AcademicTraining


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
            'last_name',
            'email',
            'cargo',
            'cellphone',
            'cedula',
            'username',
            'groups',
        ]
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name': TextInput(attrs={'class': 'form-control', 'required': True}),
            'email': EmailInput(attrs={'class': 'form-control', 'required': True}),
            'cargo': TextInput(attrs={'class': 'form-control'}),
            'cellphone': TextInput(attrs={'class': 'form-control'}),
            'cedula': TextInput(attrs={'class': 'form-control'}),
            'username': TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'groups': SelectMultiple(attrs={'class': 'form-control', 'required': True}),
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_staff']

        help_texts = {
            'groups': 'Seleccione perfil del usuario',
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


# Inactivar Usuario
class UserInactiveForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = User
        fields = 'is_active',
        widgets = {
            'is_active': TextInput(attrs={'class': 'form-control', 'hidden': True}),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                data = form.save(commit=False)
                data.is_active = False
                data.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


# Activar usuario
class UserActiveForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = User
        fields = 'is_active',
        widgets = {
            'is_active': TextInput(attrs={'class': 'form-control', 'hidden': True}),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                data = form.save(commit=False)
                data.is_active = True
                data.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


# Edición de perfil por usuario autenticado
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
            'address_user',
            'date_birth'
        ]
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name': TextInput(attrs={'class': 'form-control', 'required': True}),
            'email': EmailInput(attrs={'class': 'form-control', 'required': True}),
            'email_person': EmailInput(attrs={'class': 'form-control'}),
            'cargo': TextInput(attrs={'class': 'form-control'}),
            'cellphone': TextInput(attrs={'class': 'form-control'}),
            'cedula': TextInput(attrs={'class': 'form-control'}),
            'address_user': TextInput(attrs={'class': 'form-control'}),
            'date_birth': DateInput(format='%Y-%m-%d', attrs={
                'id': 'date_birth',
                'class': 'form-control datepicker',
                'required': True
            })
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


# Registro de formación académica
class AcademicTrainingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = AcademicTraining
        fields = [
            'academic_title',
            'academic_institution',
            # 'date_graduation',
            'file_diploma',
        ]
        widgets = {
            'academic_title': TextInput(attrs={'class': 'form-control', 'required': True}),
            'academic_institution': TextInput(attrs={'class': 'form-control', 'required': True}),
            'file_diploma': FileInput(),
            # 'date_graduation': DateInput(format='%Y-%m-%d', attrs={
            #     'id': 'date_graduation',
            #     'class': 'form-control datepicker',
            #     'required': True
            # })
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                data = form.save(commit=False)
                data.user_id = self.request
                data.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


# Editar registro de formación académica
class AcademicTrainingUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = AcademicTraining
        fields = [
            'academic_title',
            'academic_institution',
            'date_graduation',
            'file_diploma',
        ]
        widgets = {
            'academic_title': TextInput(attrs={'class': 'form-control', 'required': True}),
            'academic_institution': TextInput(attrs={'class': 'form-control', 'required': True}),
            'file_diploma': FileInput(),
            'date_graduation': DateInput(format='%Y-%m-%d', attrs={
                'id': 'date_graduation',
                'class': 'form-control datepicker',
                'required': True
            })
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
