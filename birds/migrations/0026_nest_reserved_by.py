# Generated by Django 3.2 on 2024-01-24 20:42

import birds.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('birds', '0025_nest_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='nest',
            name='reserved_by',
            field=models.ForeignKey(blank=True, help_text='mark nest as reserved for a specific user', null=True, on_delete=models.SET(birds.models.get_sentinel_user), to=settings.AUTH_USER_MODEL),
        ),
    ]