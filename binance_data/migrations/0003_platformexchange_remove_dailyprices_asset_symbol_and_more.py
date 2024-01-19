# Generated by Django 4.1.3 on 2024-01-19 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('binance_data', '0002_dailyprices_request_time_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlatformExchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, default='not_set', max_length=50, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='dailyprices',
            name='asset_symbol',
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, default='not_set', max_length=50, unique=True)),
                ('platform_exchange', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='binance_data.platformexchange')),
            ],
        ),
        migrations.CreateModel(
            name='AssetSymbol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50)),
                ('asset_full_name', models.CharField(blank=True, max_length=100, null=True)),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='binance_data.sector')),
            ],
        ),
        migrations.AddField(
            model_name='dailyprices',
            name='symbol',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='binance_data.assetsymbol'),
        ),
    ]
