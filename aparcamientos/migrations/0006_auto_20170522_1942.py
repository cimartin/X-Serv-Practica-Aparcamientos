# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0005_auto_20170522_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparcamientos',
            name='latitud',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='aparcamientos',
            name='longitud',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='aparcamientos',
            name='telefono',
            field=models.CharField(max_length=20),
        ),
    ]
