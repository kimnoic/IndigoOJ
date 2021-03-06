# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-12 08:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('OJ', '0003_auto_20161115_0618'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('assignlimit', models.DateTimeField()),
                ('starttime', models.DateTimeField()),
                ('endtime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ContestLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.IntegerField()),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OJ.User')),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OJ.Contest')),
            ],
        ),
        migrations.CreateModel(
            name='ContestProblem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.IntegerField()),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OJ.Contest')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OJ.Problem')),
            ],
        ),
        migrations.CreateModel(
            name='ContestProblemStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField()),
                ('starttime', models.DateTimeField(auto_now_add=True)),
                ('endtime', models.DateTimeField()),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OJ.User')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OJ.ContestProblem')),
            ],
        ),
        migrations.AddField(
            model_name='contestlog',
            name='problemsolved',
            field=models.ManyToManyField(to='OJ.ContestProblem'),
        ),
        migrations.AddField(
            model_name='contest',
            name='candidates',
            field=models.ManyToManyField(through='OJ.ContestLog', to='OJ.User'),
        ),
    ]
