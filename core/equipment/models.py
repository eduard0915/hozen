from datetime import date

from crum import get_current_user
from django.db import models

from core.models import BaseModel

FREQUENCY = [
    (3, 3),
    (6, 6),
    (9, 9),
    (12, 12),
    (18, 18),
    (24, 24),
]


# Equipos
class Equipment(BaseModel):
    code = models.CharField(max_length=30, verbose_name='Código')
    description = models.CharField(max_length=200, verbose_name='Descripción')
    serial = models.CharField(max_length=50, verbose_name='Serial')
    fix_active = models.CharField(max_length=50, verbose_name='Activo Fijo')
    maker = models.CharField(max_length=100, verbose_name='Fabricante')
    location = models.CharField(max_length=300, verbose_name='Ubicación', null=True, blank=True)
    date_manufactured = models.DateField(verbose_name='Fecha de Fabricación')
    date_entry = models.DateField(verbose_name='Fecha de Ingreso')
    use_time = models.FloatField(verbose_name='Tiempo de Uso')
    manufacturer_manual = models.FileField(
        upload_to='equipment_manual/%Y%m%d', verbose_name='Manual de Fabricante', null=True, blank=True)
    manufacturer_docs = models.FileField(
        upload_to='equipment_docs/%Y%m%d', verbose_name='Documentos Anexos de Fabricante', null=True, blank=True)
    status = models.BooleanField(default=True, verbose_name='Estado')
    frequency_maintenance = models.SmallIntegerField(verbose_name='Frecuencia Mantenimiento')
    calibration = models.BooleanField(default=False, verbose_name='Requiere Calibración?')
    frequency_calibration = models.SmallIntegerField(verbose_name='Frecuencia Calibración', null=True, blank=True)

    def __str__(self):
        return f'{self.code} {self.description}'

    class Meta:
        db_table = 'Equipment'
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipments'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, *args, **kwargs):
        today = date.today()
        diff_days = today - self.date_manufactured
        months = float(diff_days.days/365)
        self.use_time = round(months, 1)
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        self.code = self.code.upper()
        return super(Equipment, self).save(*args, **kwargs)

