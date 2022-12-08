from crum import get_current_user
from dateutil.relativedelta import relativedelta
from django.db import models

from core.equipment.models import Equipment
from core.models import BaseModel


# Calibración
class Calibration(BaseModel):
    certificate_number = models.CharField(max_length=30, verbose_name='Número de Certificado')
    date_calibration = models.DateField(verbose_name='Fecha')
    date_calibration_next = models.DateField(null=True, blank=True)
    calibration_certificate = models.FileField(
        upload_to='calibration_certificate/%Y%m%d', verbose_name='Certificado de Calibración', null=True, blank=True)
    comments_calibration = models.TextField(verbose_name='Observaciones')
    calibration_made_by = models.CharField(max_length=300, verbose_name='Realizado por', null=True, blank=True)
    equipment = models.ForeignKey(Equipment, verbose_name='Equipo', on_delete=models.CASCADE, related_name='+')

    def __str__(self):
        return self.certificate_number

    class Meta:
        db_table = 'Calibration'
        verbose_name = 'Calibration'
        verbose_name_plural = 'Calibrations'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, *args, **kwargs):
        user = get_current_user()
        self.date_calibration_next = self.date_calibration + relativedelta(months=self.equipment.frequency_calibration)
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        return super(Calibration, self).save(*args, **kwargs)
