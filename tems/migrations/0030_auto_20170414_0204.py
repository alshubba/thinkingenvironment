# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-14 02:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tems', '0029_auto_20170414_0204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshopevaluation',
            name='workshop_registration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tems.WorkshopRegistration'),
        ),
    ]
