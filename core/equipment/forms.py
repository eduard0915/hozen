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
        fields = [
            'code',
            'description',
            'serial',
            'maker',
            'date_manufactured',
            'date_entry',
            'frequency_maintenance',
            'calibration',
            'frequency_calibration',
        ]
        widgets = {
            'code': TextInput(attrs={'class': 'form-control', 'required': True}),
            'description': TextInput(attrs={'class': 'form-control', 'required': True}),
            'serial': TextInput(attrs={'class': 'form-control', 'required': True}),
            'maker': TextInput(attrs={'class': 'form-control', 'required': True}),
            'date_manufactured': DateInput(attrs={'class': 'form-control', 'required': True}),
            'date_entry': DateInput(attrs={'class': 'form-control', 'required': True}),
            'frequency_maintenance': NumberInput(attrs={'class': 'form-control', 'required': True}),
            'calibration': NullBooleanSelect(attrs={'class': 'form-control', 'required': True}),
            'frequency_calibration': NumberInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'frequency_maintenance': 'Meses',
            'frequency_calibration': 'Meses',
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
