# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-14 21:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0013_auto_20180214_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='username',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
