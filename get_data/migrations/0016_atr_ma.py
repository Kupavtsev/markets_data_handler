# Generated by Django 4.1.3 on 2024-03-11 14:05

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_data', '0015_rename_request_time_two_hours_end_of_candle_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='atr',
            name='ma',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True, null=True), blank=True, default=list, null=True, size=None, verbose_name='MA Levels'),
        ),
    ]
