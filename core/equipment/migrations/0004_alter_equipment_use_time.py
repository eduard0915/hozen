# Generated by Django 4.1.3 on 2022-12-04 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0003_alter_equipment_use_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='use_time',
            field=models.FloatField(default=1, verbose_name='Tiempo de Uso'),
            preserve_default=False,
        ),
    ]