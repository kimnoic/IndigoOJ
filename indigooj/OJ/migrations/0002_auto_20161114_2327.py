# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-14 14:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OJ', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='name',
        ),
        migrations.AddField(
            model_name='problem',
            name='sampleinput',
            field=models.CharField(default=b'', max_length=500),
        ),
        migrations.AddField(
            model_name='problem',
            name='sampleoutput',
            field=models.CharField(default=b'', max_length=500),
        ),
        migrations.AlterField(
            model_name='problem',
            name='sample',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
