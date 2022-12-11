# Generated by Django 4.1.4 on 2022-12-09 01:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address_user',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Dirección'),
        ),
        migrations.AddField(
            model_name='user',
            name='date_birth',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Nacimiento'),
        ),
        migrations.CreateModel(
            name='AcademicTraining',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('academic_title', models.CharField(max_length=300, verbose_name='Título Obtenido')),
                ('academic_institution', models.CharField(max_length=200, verbose_name='Institución Académica')),
                ('date_graduation', models.DateField(verbose_name='Fecha de Graduación')),
                ('file_diploma', models.FileField(upload_to='file_diploma/%Y%m%d', verbose_name='Diploma')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='')),
                ('user_creation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_creation', to=settings.AUTH_USER_MODEL)),
                ('user_updated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
