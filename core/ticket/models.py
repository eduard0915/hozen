from crum import get_current_user
from django.db import models

from core.equipment.models import Equipment
from core.models import BaseModel


# Solicitudes de mantenimiento
class Ticket(BaseModel):
    ticket = models.CharField(max_length=30, verbose_name='Ubicación')
    location = models.CharField(max_length=30, verbose_name='Ubicación')
    type_ticket = models.CharField(max_length=30, verbose_name='Tipo de Solicitud')
    group_ticket = models.CharField(max_length=30, verbose_name='Grupo')
    subject = models.CharField(max_length=30, verbose_name='Asunto')
    status_ticket = models.CharField(max_length=30, verbose_name='', default='Abierto')
    date_close = models.DateField(verbose_name='Fecha de Cierre', null=True, blank=True)
    image_ticket = models.ImageField(
        upload_to='physical_record/%Y%m%d', verbose_name='Imagen Solicitud', null=True, blank=True)
    description_ticket = models.TextField(verbose_name='Descripción de la Solicitud')
    equipment = models.ForeignKey(Equipment, verbose_name='Activo Fijo', on_delete=models.CASCADE)
    comments = models.CharField(max_length=500, verbose_name='Observaciones', null=True, blank=True)

    def __str__(self):
        return self.ticket

    class Meta:
        db_table = 'Ticket'
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, *args, **kwargs):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        return super(Ticket, self).save(*args, **kwargs)
