# Generated by Django 4.1.3 on 2024-03-07 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('get_data', '0013_dailyprices_atr_levels'),
    ]

    operations = [
        migrations.CreateModel(
            name='Two_Hours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_date', models.DateField()),
                ('time_of_candle', models.DateTimeField(blank=True, null=True)),
                ('price_open', models.FloatField(blank=True, null=True)),
                ('price_high', models.FloatField(blank=True, null=True)),
                ('price_low', models.FloatField(blank=True, null=True)),
                ('price_close', models.FloatField(blank=True, null=True)),
                ('volume', models.FloatField(blank=True, null=True)),
                ('request_time', models.DateTimeField(blank=True, null=True)),
                ('symbol', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='get_data.assetsymbol')),
            ],
            options={
                'verbose_name': 'Two Hours',
                'verbose_name_plural': 'Two Hours',
                'db_table': 'two_hours_prices',
                'ordering': ['-session_date'],
                'unique_together': {('symbol', 'time_of_candle')},
            },
        ),
    ]