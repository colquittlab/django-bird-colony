# Generated by Django 3.2 on 2024-01-23 00:05

import birds.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('birds', '0022_animal_age_days'),
    ]

    operations = [
        migrations.CreateModel(
            name='Egg',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('lay_date', models.DateTimeField(auto_now_add=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('nest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='egg_nest', to='birds.nest')),
            ],
        ),
        migrations.CreateModel(
            name='EggEventCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('count', models.SmallIntegerField(choices=[(0, '0'), (-1, '-1'), (1, '+1')], default=0, help_text='1: egg laid; -1: egg removed; 0: no change')),
                ('category', models.CharField(blank=True, choices=[('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], max_length=2, null=True)),
            ],
            options={
                'verbose_name_plural': 'egg event codes',
                'ordering': ['name'],
            },
        ),
        migrations.AlterField(
            model_name='animal',
            name='nest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='nests', to='birds.nest'),
        ),
        migrations.CreateModel(
            name='ParentEgg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('egg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='birds.egg')),
                ('parent', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='birds.animal')),
            ],
        ),
        migrations.CreateModel(
            name='EggEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('egg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='birds.egg')),
                ('entered_by', models.ForeignKey(on_delete=models.SET(birds.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='birds.eggeventcode')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.AddField(
            model_name='egg',
            name='parents',
            field=models.ManyToManyField(related_name='egg_children', through='birds.ParentEgg', to='birds.Animal'),
        ),
        migrations.AddField(
            model_name='egg',
            name='reserved_by',
            field=models.ForeignKey(blank=True, help_text='mark a bird as reserved for a specific user', null=True, on_delete=models.SET(birds.models.get_sentinel_user), to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='egg',
            name='species',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='birds.species'),
        ),
    ]
