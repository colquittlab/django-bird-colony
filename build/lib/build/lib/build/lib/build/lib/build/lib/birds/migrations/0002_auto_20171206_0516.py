# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-06 05:16
from __future__ import unicode_literals

import birds.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('birds', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nest',
            fields=[
                ('location_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='birds.Location')),
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('nest_bands', models.CharField(blank=True, max_length=15, null=True)),
            ],
            bases=('birds.location',),
        ),
        # migrations.CreateModel(
        #     name='NestEvent',
        #     fields=[
        #         ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('date', models.DateField(default=datetime.date.today)),
        #         ('number', models.SmallIntegerField(default=0)),
        #         ('entered_by', models.ForeignKey(on_delete=models.SET(birds.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
        #         ('nest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='birds.Nest')),
        #     ],
        #     options={
        #         'ordering': ['-date'],
        #     },
        # ),
        # migrations.CreateModel(
        #     name='NestStatus',
        #     fields=[
        #         ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('name', models.CharField(max_length=16, unique=True)),
        #         ('description', models.TextField()),
        #     ],
        #     options={
        #         'verbose_name_plural': 'nest status codes',
        #         'ordering': ['name'],
        #     },
        # ),
        # migrations.DeleteModel(
        #     name='DataCollection',
        # ),
        # migrations.DeleteModel(
        #     name='DataType',
        # ),
        # migrations.AlterModelOptions(
        #     name='location',
        #     options={},
        # ),
        # migrations.AddField(
        #     model_name='animal',
        #     name='band',
        #     field=models.CharField(default=None, max_length=25),
        #     preserve_default=False,
        # ),
        # migrations.AddField(
        #     model_name='animal',
        #     name='band_color2',
        #     field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='b2', to='birds.Color'),
        # ),
        # migrations.AddField(
        #     model_name='animal',
        #     name='band_number2',
        #     field=models.IntegerField(blank=True, null=True),
        # ),
        # migrations.AddField(
        #     model_name='animal',
        #     name='location',
        #     field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='locations', to='birds.Location'),
        # ),
        # migrations.AlterField(
        #     model_name='animal',
        #     name='band_color',
        #     field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='b1', to='birds.Color'),
        # ),
        # migrations.AddField(
        #     model_name='nestevent',
        #     name='status',
        #     field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='birds.NestStatus'),
        # ),
        # migrations.AddField(
        #     model_name='nest',
        #     name='dam',
        #     field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='birds.Animal'),
        # ),
        # migrations.AddField(
        #     model_name='nest',
        #     name='sire',
        #     field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='birds.Animal'),
        # ),
        # migrations.AddField(
        #     model_name='animal',
        #     name='nest',
        #     field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='nests', to='birds.Nest'),
        # ),
    ]
