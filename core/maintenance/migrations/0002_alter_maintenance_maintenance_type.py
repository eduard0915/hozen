# Generated by Django 4.1.3 on 2022-12-05 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenance',
            name='maintenance_type',
            field=models.CharField(max_length=30, verbose_name='Tipo de Mantenimiento'),
        ),
    ]