from django.forms import *

from core.maintenance.models import Maintenance


# Creación de Equipo
class MaintenanceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Maintenance
        fields = [
            'maintenance_number',
            'date_maintenance',
            'equipment',
            'maintenance_type',
            'description_maintenance',
            'chances_pieces',
            'physical_record',
            'made_by',
            'contractor',
        ]
        widgets = {
            'maintenance_number': TextInput(attrs={'class': 'form-control', 'required': True}),
            'contractor': TextInput(attrs={'class': 'form-control'}),
            'equipment': Select(attrs={'class': 'form-control', 'required': True}),
            'chances_pieces': Textarea(attrs={'class': 'form-control', 'required': True, 'rows': 3}),
            'description_maintenance': Textarea(attrs={'class': 'form-control', 'required': True, 'rows': 3}),
            'physical_record': FileInput(),
            'maintenance_type': Select(attrs={'class': 'form-control', 'required': True}),
            'made_by': Select(attrs={'class': 'form-control'}),
            'date_maintenance': DateInput(format='%Y-%m-%d', attrs={
                'id': 'date_maintenance',
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
