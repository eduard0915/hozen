# Generated by Django 4.1.3 on 2022-12-05 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0002_alter_maintenance_maintenance_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenance',
            name='contractor',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Contratista'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='date_maintenance_next',
            field=models.DateField(blank=True, null=True),
        ),
    ]
