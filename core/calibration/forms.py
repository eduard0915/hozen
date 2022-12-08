from django.forms import *

from core.calibration.models import Calibration


# Creación de registro de calibración
class CalibrationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Calibration
        fields = [
            'date_calibration',
            'equipment',
            'certificate_number',
            'calibration_certificate',
            'calibration_made_by',
            'comments_calibration',
        ]
        widgets = {
            'certificate_number': TextInput(attrs={'class': 'form-control', 'required': True}),
            'calibration_made_by': TextInput(attrs={'class': 'form-control', 'required': True}),
            'equipment': Select(attrs={'class': 'form-control', 'required': True}),
            'comments_calibration': Textarea(attrs={'class': 'form-control', 'required': True, 'rows': 3}),
            'calibration_certificate': FileInput(),
            'date_calibration': DateInput(format='%Y-%m-%d', attrs={
                'id': 'date_calibration',
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
