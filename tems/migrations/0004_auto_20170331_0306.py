# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-31 03:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tems', '0003_auto_20170330_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thinkingenvuser',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='thinkingenvuser',
            name='country',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='thinkingenvuser',
            name='marital_status',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='thinkingenvuser',
            name='neighborhood',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='thinkingenvuser',
            name='phone',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='thinkingenvuser',
            name='sex',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]