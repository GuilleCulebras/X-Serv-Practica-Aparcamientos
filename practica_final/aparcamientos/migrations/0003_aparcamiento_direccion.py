# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-16 17:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0002_auto_20170516_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='aparcamiento',
            name='direccion',
            field=models.CharField(default='', max_length=120),
        ),
    ]
