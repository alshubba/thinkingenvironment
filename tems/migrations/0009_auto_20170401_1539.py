# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-01 15:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tems', '0008_infographic_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thinkingenvuser',
            name='marital_status',
            field=models.CharField(blank=True, choices=[('married', 'Married'), ('single', 'Single')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='thinkingenvuser',
            name='phone',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='thinkingenvuser',
            name='sex',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=255, null=True),
        ),
    ]