# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-03-07 16:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tems', '0044_ambassadorcountry_flag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ambassadorcountry',
            name='flag',
            field=models.ImageField(blank=True, null=True, upload_to='countries/'),
        ),
    ]
