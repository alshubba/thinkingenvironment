# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-30 20:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tems', '0002_auto_20170330_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thinkingenvuser',
            name='city',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='thinkingenvuser',
            name='country',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='thinkingenvuser',
            name='marital_status',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='thinkingenvuser',
            name='neighborhood',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='thinkingenvuser',
            name='phone',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='thinkingenvuser',
            name='sex',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
