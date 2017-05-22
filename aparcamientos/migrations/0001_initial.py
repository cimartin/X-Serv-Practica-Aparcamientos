# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-08 23:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aparcamientos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(default='')),
                ('direccion', models.TextField(default='')),
                ('descripcion', models.TextField(default='')),
                ('barrio', models.TextField(default='')),
                ('url', models.TextField(default='')),
                ('latitud', models.FloatField(default='')),
                ('longitud', models.FloatField(default='')),
                ('accesibilidad', models.IntegerField(default=0)),
                ('email', models.TextField(default='')),
                ('phone', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Comentarios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(default='')),
                ('aparcamiento_comentado', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='aparcamientos.Aparcamientos')),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Configuracion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.TextField(default='default')),
                ('bg_color', models.CharField(default='blue', max_length=32)),
                ('tamano_ltr', models.IntegerField(default=12)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Seleccionados',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('aparcamiento_seleccionado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aparcamientos.Aparcamientos')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]