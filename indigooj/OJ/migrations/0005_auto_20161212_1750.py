# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-12 08:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OJ', '0004_auto_20161212_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestlog',
            name='problemsolved',
            field=models.ManyToManyField(blank=True, to='OJ.ContestProblem'),
        ),
    ]
