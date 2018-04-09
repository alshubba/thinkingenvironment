# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-03-30 19:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tems', '0046_auto_20180329_2106'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('avatar', models.ImageField(null=True, upload_to='experts/')),
                ('twitter', models.CharField(blank=True, max_length=255, null=True)),
                ('facebook', models.CharField(blank=True, max_length=255, null=True)),
                ('youtube', models.CharField(blank=True, max_length=255, null=True)),
                ('snapchat', models.CharField(blank=True, max_length=255, null=True)),
                ('instgram', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='auditlog',
            name='event',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='auditlog',
            name='title',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]