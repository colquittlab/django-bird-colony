# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-14 18:31
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('birds', '0010_animal_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Claim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('uuid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='birds.Animal')),
            ],
            managers=[
                ('latest', django.db.models.manager.Manager()),
            ],
        ),
    ]
