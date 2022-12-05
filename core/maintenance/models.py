from datetime import datetime, date

from crum import get_current_user
from django.db import models

from core.equipment.models import Equipment
from core.models import BaseModel
from core.user.models import User


TYPE = [
    ('Correctivo', 'Correctivo'),
    ('Preventivo', 'Preventivo'),
]


def increment_number_maintenance():
    year = datetime.now().strftime('%Y')
    last_maintenance = Maintenance.objects.all().order_by('id').last()
    if not last_maintenance or last_maintenance.date_creation.strftime('%Y') != date.today().strftime('%Y'):
        return 'OT-' + year + '-' + '1'
    number_maintenance = last_maintenance.maintenance_number
    number_maintenance_int = int(number_maintenance.split('-')[2])
    new_number_maintenance_int = number_maintenance_int + 1
    new_number_maintenance = 'OT-' + year + '-' + str(new_number_maintenance_int)
    return new_number_maintenance


# Mantenimiento
class Maintenance(BaseModel):
    maintenance_number = models.CharField(max_length=30, verbose_name='', default=increment_number_maintenance)
    maintenance_type = models.CharField(max_length=30, verbose_name='Tipo de Mantenimiento')
    date_maintenance = models.DateField(verbose_name='Fecha')
    date_maintenance_next = models.DateField(null=True, blank=True)
    physical_record = models.FileField(
        upload_to='physical_record/%Y%m%d', verbose_name='Registro Físico', null=True, blank=True)
    description_maintenance = models.TextField(verbose_name='Detalle de Mantenimiento')
    chances_pieces = models.TextField(verbose_name='Piezas o Partes Reemplazadas')
    equipment = models.ForeignKey(Equipment, verbose_name='Equipo', on_delete=models.CASCADE)
    made_by = models.ForeignKey(User, verbose_name='Realizado por', on_delete=models.CASCADE)
    contractor = models.CharField(max_length=300, verbose_name='Contratista', null=True, blank=True)

    def __str__(self):
        return self.maintenance_number

    class Meta:
        db_table = 'Maintenance'
        verbose_name = 'Maintenance'
        verbose_name_plural = 'Maintenances'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, *args, **kwargs):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        return super(Maintenance, self).save(*args, **kwargs)
