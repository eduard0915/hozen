from datetime import date

from crum import get_current_user
from django.db import models

from core.models import BaseModel


# Marca modelo equipos
class EquipmentMarkModel(BaseModel):
    description = models.CharField(max_length=200, verbose_name='Descripción')
    mark = models.CharField(max_length=50, verbose_name='Marca')
    model = models.CharField(max_length=100, verbose_name='Modelo')
    maker = models.CharField(max_length=100, verbose_name='Fabricante')

    def __str__(self):
        return f'{self.description} {self.mark} {self.model}'

    class Meta:
        db_table = 'EquipmentMarkModel'
        verbose_name = 'EquipmentMarkModel'
        verbose_name_plural = 'EquipmentMarkModels'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, *args, **kwargs):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        return super(EquipmentMarkModel, self).save(*args, **kwargs)


# Equipos
class Equipment(BaseModel):
    description_equipment = models.ForeignKey(EquipmentMarkModel, verbose_name='Descripción', on_delete=models.CASCADE)
    serial = models.CharField(max_length=50, verbose_name='Serial')
    fix_active = models.CharField(max_length=50, verbose_name='Activo Fijo')
    location = models.CharField(max_length=300, verbose_name='Ubicación', null=True, blank=True)
    date_manufactured = models.DateField(verbose_name='Fecha de Fabricación')
    date_entry = models.DateField(verbose_name='Fecha de Ingreso')
    use_time = models.FloatField(verbose_name='Tiempo de Uso')
    manufacturer_manual = models.FileField(
        upload_to='equipment_manual/%Y%m%d', verbose_name='Manual de Fabricante', null=True, blank=True)
    manufacturer_docs = models.FileField(
        upload_to='equipment_docs/%Y%m%d', verbose_name='Documentos Anexos de Fabricante', null=True, blank=True)
    status = models.BooleanField(default=True, verbose_name='Estado')
    frequency_maintenance = models.PositiveIntegerField(verbose_name='Frecuencia Mantenimiento')
    calibration = models.BooleanField(default=False, verbose_name='Requiere Calibración?')
    frequency_calibration = models.PositiveIntegerField(verbose_name='Frecuencia Calibración', null=True, blank=True)
    photo_equipment = models.ImageField(verbose_name='Imagen del Equipo', upload_to='photo_equipment/%Y%m%d', null=True, blank=True)
    useful_life = models.PositiveIntegerField(verbose_name='Vida Util')
    risk_classification = models.CharField(max_length=20, verbose_name='Clasificación de Riesgo')
    acquisition = models.CharField(max_length=50, verbose_name='Adquisición')
    register_regulatory = models.CharField(max_length=100, verbose_name='Registro Regulatorio', null=True, blank=True)

    def __str__(self):
        return self.description_equipment

    class Meta:
        db_table = 'Equipment'
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipments'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, *args, **kwargs):
        today = date.today()
        diff_days = today - self.date_manufactured
        months = float(diff_days.days/365)
        self.use_time = round(months, 1)
        self.frequency_calibration = int(self.frequency_calibration)
        self.frequency_maintenance = int(self.frequency_maintenance)
        self.useful_life = int(self.useful_life)
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        return super(Equipment, self).save(*args, **kwargs)
