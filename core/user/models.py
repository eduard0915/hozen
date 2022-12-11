from crum import get_current_user
from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import BaseModel


# Usuarios
class User(AbstractUser):
    cedula = models.CharField(max_length=15, null=True, blank=True, unique=False, verbose_name='Cédula')
    cargo = models.CharField(max_length=50, null=True, blank=True, verbose_name='Cargo')
    cellphone = models.CharField(max_length=10, null=True, blank=True, verbose_name='N° Celular')
    email_person = models.EmailField(null=True, blank=True, verbose_name='Email Personal')
    address_user = models.CharField(max_length=100, verbose_name='Dirección', null=True, blank=True)
    date_birth = models.DateField(verbose_name='Fecha de Nacimiento', null=True, blank=True)

    def __str__(self):
        return f'{self.get_full_name()}, {self.cargo}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        self.cargo = self.cargo.capitalize() if self.cargo is not None else self.cargo == 'Cargo'
        if self.username is not int:
            self.username = self.username.lower()
        return super(User, self).save(*args, **kwargs)


# Formación académica
class AcademicTraining(BaseModel):
    academic_title = models.CharField(max_length=300, verbose_name='Título Obtenido')
    academic_institution = models.CharField(max_length=200, verbose_name='Institución Académica')
    date_graduation = models.DateField(verbose_name='Fecha de Graduación', null=True, blank=True)
    file_diploma = models.FileField(upload_to='file_diploma/%Y%m%d', verbose_name='Diploma')
    user = models.ForeignKey(User, verbose_name='', on_delete=models.CASCADE)

    def __str__(self):
        return self.academic_title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, *args, **kwargs):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        return super(AcademicTraining, self).save(*args, **kwargs)
