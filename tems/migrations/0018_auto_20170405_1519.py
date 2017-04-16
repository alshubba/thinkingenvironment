# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-05 15:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tems', '0017_workshoprequest_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('presenter', models.CharField(max_length=255)),
                ('begin_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('price', models.IntegerField(default=0)),
                ('poster', models.ImageField(upload_to='workshops/')),
            ],
        ),
        migrations.AlterField(
            model_name='workshoprequest',
            name='director_email',
            field=models.EmailField(max_length=255),
        ),
        migrations.AlterField(
            model_name='workshoprequest',
            name='trainees_sex',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('mixed', 'Mixed')], max_length=255),
        ),
    ]