# Generated by Django 4.1.3 on 2024-01-19 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DailyPrices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_symbol', models.CharField(max_length=50, verbose_name='symbol')),
                ('session_date', models.DateTimeField(unique=True)),
                ('price_day_open', models.FloatField(blank=True, null=True)),
                ('price_day_high', models.FloatField(blank=True, null=True)),
                ('price_day_low', models.FloatField(blank=True, null=True)),
                ('price_day_close', models.FloatField(blank=True, null=True)),
                ('day_volume', models.FloatField(blank=True, null=True)),
                ('day_true_range', models.FloatField(blank=True, null=True)),
                ('day_average_true_range', models.FloatField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Symbol Daily Prices (TR, ATR)',
                'verbose_name_plural': 'Symbol Daily Prices (TR, ATR)',
                'db_table': 'daily_prices',
                'ordering': ['session_date'],
            },
        ),
    ]
