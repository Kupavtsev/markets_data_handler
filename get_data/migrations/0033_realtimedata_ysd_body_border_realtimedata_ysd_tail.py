# Generated by Django 4.1.3 on 2024-03-27 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_data', '0032_realtimedata_ysd_body_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='realtimedata',
            name='ysd_body_border',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='realtimedata',
            name='ysd_tail',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
