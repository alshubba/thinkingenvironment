# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-13 15:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tems', '0025_auto_20170412_0226'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmbassadorRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('nationality', models.CharField(max_length=255)),
                ('place_of_stay', models.CharField(max_length=255)),
                ('education', models.CharField(max_length=255)),
                ('about_you', models.CharField(max_length=255)),
                ('what_can_you_provide', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('open', 'Open'), ('closed', 'Closed')], default='open', max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tems.ThinkingEnvUser')),
            ],
        ),
    ]
