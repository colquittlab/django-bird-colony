# Generated by Django 4.2.9 on 2024-01-19 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0016_auto_20180508_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='call_speed',
            field=models.FloatField(blank=True, max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='animal',
            name='repeats',
            field=models.CharField(blank=True, choices=[('Y', 'yes'), ('N', 'no')], max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='animal',
            name='seqvar',
            field=models.CharField(blank=True, choices=[('Y', 'yes'), ('N', 'no')], max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='animal',
            name='song_speed',
            field=models.FloatField(blank=True, max_length=4, null=True),
        ),
        migrations.CreateModel(
            name='GeneticParent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genchild', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='birds.animal')),
                ('genparent', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='birds.animal')),
            ],
        ),
    ]
