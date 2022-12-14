# Generated by Django 4.1.4 on 2022-12-14 01:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('equipment', '0009_alter_equipment_photo_equipment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('ticket', models.CharField(max_length=30, verbose_name='Ubicación')),
                ('location', models.CharField(max_length=30, verbose_name='Ubicación')),
                ('type_ticket', models.CharField(max_length=30, verbose_name='Tipo de Solicitud')),
                ('group_ticket', models.CharField(max_length=30, verbose_name='Grupo')),
                ('subject', models.CharField(max_length=30, verbose_name='Asunto')),
                ('status_ticket', models.CharField(default='Abierto', max_length=30, verbose_name='')),
                ('date_close', models.DateField(blank=True, null=True, verbose_name='Fecha de Cierre')),
                ('image_ticket', models.ImageField(blank=True, null=True, upload_to='physical_record/%Y%m%d', verbose_name='Imagen Solicitud')),
                ('description_ticket', models.TextField(verbose_name='Descripción de la Solicitud')),
                ('comments', models.CharField(blank=True, max_length=500, null=True, verbose_name='Observaciones')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipment.equipment', verbose_name='Activo Fijo')),
                ('user_creation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_creation', to=settings.AUTH_USER_MODEL)),
                ('user_updated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ticket',
                'verbose_name_plural': 'Tickets',
                'db_table': 'Ticket',
            },
        ),
    ]