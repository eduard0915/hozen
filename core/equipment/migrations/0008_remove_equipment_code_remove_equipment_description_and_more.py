# Generated by Django 4.1.4 on 2022-12-13 16:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('equipment', '0007_equipment_photo_equipment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipment',
            name='code',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='description',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='maker',
        ),
        migrations.AddField(
            model_name='equipment',
            name='acquisition',
            field=models.CharField(default=1, max_length=50, verbose_name='Adquisición'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='equipment',
            name='risk_classification',
            field=models.CharField(default=1, max_length=20, verbose_name='Clasificación de Riesgo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='equipment',
            name='useful_life',
            field=models.PositiveIntegerField(default=1, verbose_name='Vida Util'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='EquipmentMarkModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('description', models.CharField(max_length=200, verbose_name='Descripción')),
                ('mark', models.CharField(max_length=50, verbose_name='Marca')),
                ('model', models.CharField(max_length=100, verbose_name='Modelo')),
                ('maker', models.CharField(max_length=100, verbose_name='Fabricante')),
                ('user_creation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_creation', to=settings.AUTH_USER_MODEL)),
                ('user_updated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'EquipmentMarkModel',
                'verbose_name_plural': 'EquipmentMarkModels',
                'db_table': 'EquipmentMarkModel',
            },
        ),
        migrations.AddField(
            model_name='equipment',
            name='description_equipment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='equipment.equipmentmarkmodel', verbose_name='Descripción'),
            preserve_default=False,
        ),
    ]
