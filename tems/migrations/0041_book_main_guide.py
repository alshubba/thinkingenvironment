# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-14 15:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tems', '0040_thinkingenvuser_booklet_download_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='main_guide',
            field=models.BooleanField(default=False),
        ),
    ]