# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-14 19:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0011_claim'),
    ]

    operations = [
        migrations.RenameField(
            model_name='claim',
            old_name='uuid',
            new_name='animal',
        ),
    ]
