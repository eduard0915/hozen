from django.forms import *

from core.equipment.models import *


# Creación de Equipo
class EquipmentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Equipment
        CHOICES_SELECT = [(True, 'Si'), (False, 'No')]
        FREQUENCY = [
            (None, ''),
            (1, 'Mensual'),
            (2, 'Bimensual'),
            (3, 'Trimestral'),
            (6, 'Semestral'),
            (12, 'Anual'),
            (24, 'Bianual')
        ]
        fields = [
            'code',
            'description',
            'serial',
            'maker',
            'date_manufactured',
            'date_entry',
            'frequency_maintenance',
            'location',
            'fix_active',
            'calibration',
            'frequency_calibration',
            'manufacturer_manual',
            'manufacturer_docs',
        ]
        widgets = {
            'code': TextInput(attrs={'class': 'form-control', 'required': True}),
            'description': TextInput(attrs={'class': 'form-control', 'required': True}),
            'serial': TextInput(attrs={'class': 'form-control', 'required': True}),
            'maker': TextInput(attrs={'class': 'form-control', 'required': True}),
            'fix_active': TextInput(attrs={'class': 'form-control', 'required': True}),
            'location': TextInput(attrs={'class': 'form-control', 'required': True}),
            'frequency_maintenance': Select(attrs={'class': 'form-control', 'required': True}, choices=FREQUENCY),
            'calibration': Select(attrs={'class': 'form-control', 'required': True}, choices=CHOICES_SELECT),
            'manufacturer_manual': FileInput(),
            'manufacturer_docs': FileInput(),
            'frequency_calibration': Select(attrs={'class': 'form-control'}, choices=FREQUENCY),
            'date_manufactured': DateInput(format='%Y-%m-%d', attrs={
                'id': 'date_manufactured',
                'class': 'form-control datepicker',
                'required': True
            }),
            'date_entry': DateInput(format='%Y-%m-%d', attrs={
                'id': 'date_entry',
                'class': 'form-control datepicker',
                'required': True
            }),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                data = form.save(commit=False)
                if not data.calibration:
                    data.frequency_calibration = None
                data.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


# Equipo fuera de servicio
class EquipmentInactiveForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].label = ''
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Equipment
        fields = 'status',
        widgets = {
            'status': TextInput(attrs={'class': 'form-control', 'hidden': True}),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                data = form.save(commit=False)
                data.status = False
                data.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


# Equipo en servicio
class EquipmentActiveForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].label = ''
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Equipment
        fields = 'status',
        widgets = {
            'status': TextInput(attrs={'class': 'form-control', 'hidden': True}),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                data = form.save(commit=False)
                data.status = True
                data.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
