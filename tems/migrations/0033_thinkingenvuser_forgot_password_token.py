# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-14 15:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tems', '0032_auto_20170414_0305'),
    ]

    operations = [
        migrations.AddField(
            model_name='thinkingenvuser',
            name='forgot_password_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
