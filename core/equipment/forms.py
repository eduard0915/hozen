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
        CHOICES_RISK = [
            ('', ''),
            ('Clase I, Riesgo Bajo', 'Clase I, Riesgo Bajo'),
            ('Clase IIa, Riesgo Moderado', 'Clase IIa, Riesgo Moderado'),
            ('Clase IIb, Riesgo Alto', 'Clase IIb, Riesgo Alto'),
            ('Clase III, Riesgo Muy Alto', 'Clase III, Riesgo Muy Alto'),
        ]
        CHOICES_ACQUISITION = [('', ''), ('Propio', 'Propio'), ('Comodato', 'Comodato'), ('Préstamo', 'Préstamo')]
        fields = [
            'description_equipment',
            'serial',
            'date_manufactured',
            'date_entry',
            'location',
            'fix_active',
            'register_regulatory',
            'risk_classification',
            'acquisition',
            'useful_life',
            'calibration',
            'frequency_maintenance',
            'frequency_calibration',
            'manufacturer_manual',
            'manufacturer_docs',
            'photo_equipment',
        ]
        widgets = {
            'description_equipment': Select(attrs={'class': 'form-control', 'required': True}),
            'serial': TextInput(attrs={'class': 'form-control', 'required': True}),
            'fix_active': TextInput(attrs={'class': 'form-control', 'required': True}),
            'location': TextInput(attrs={'class': 'form-control', 'required': True}),
            'register_regulatory': TextInput(attrs={'class': 'form-control', 'required': True}),
            'frequency_maintenance': TextInput(attrs={'class': 'form-control', 'required': True}),
            'useful_life': TextInput(attrs={'class': 'form-control', 'required': True}),
            'calibration': Select(attrs={'class': 'form-control', 'required': True}, choices=CHOICES_SELECT),
            'risk_classification': Select(attrs={'class': 'form-control', 'required': True}),
            'acquisition': Select(attrs={'class': 'form-control', 'required': True}, choices=CHOICES_ACQUISITION),
            'manufacturer_manual': FileInput(),
            'manufacturer_docs': FileInput(),
            'photo_equipment': FileInput(),
            'frequency_calibration': TextInput(attrs={'class': 'form-control'}),
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

        help_texts = {
            'frequency_calibration': 'Meses',
            'frequency_maintenance': 'Meses',
            'useful_life': 'Años',
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


# Creación de Equipo Marca Modelo
class EquipmentMarkModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = EquipmentMarkModel
        fields = ['description', 'model', 'mark', 'maker']
        widgets = {
            'description': TextInput(attrs={'class': 'form-control', 'required': True}),
            'model': TextInput(attrs={'class': 'form-control', 'required': True}),
            'mark': TextInput(attrs={'class': 'form-control', 'required': True}),
            'maker': TextInput(attrs={'class': 'form-control', 'required': True})
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
