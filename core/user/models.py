from django.contrib.auth.models import AbstractUser
from django.db import models


# Creación de usuarios
class User(AbstractUser):
    cedula = models.CharField(max_length=15, null=True, blank=True, unique=False, verbose_name='Cédula')
    cargo = models.CharField(max_length=50, null=True, blank=True, verbose_name='Cargo')
    cellphone = models.CharField(max_length=10, null=True, blank=True, verbose_name='N° Celular')
    email_person = models.EmailField(null=True, blank=True, verbose_name='Email Personal')

    def __str__(self):
        return f'{self.get_full_name()}, {self.cargo}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        self.cargo = self.cargo.capitalize() if self.cargo is not None else self.cargo == 'Cargo'
        if self.username is not int:
            self.username = self.username.lower()
        return super(User, self).save(*args, **kwargs)
