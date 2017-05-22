# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0004_auto_20170513_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparcamientos',
            name='latitud',
            field=models.FloatField(default=''),
        ),
        migrations.AlterField(
            model_name='aparcamientos',
            name='longitud',
            field=models.FloatField(default=''),
        ),
        migrations.AlterField(
            model_name='aparcamientos',
            name='telefono',
            field=models.IntegerField(default=0),
        ),
    ]
