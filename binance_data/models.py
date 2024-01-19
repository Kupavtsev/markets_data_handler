from django.db import models



class PlatformExchange(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True, default='not_set')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "platform_exchange"
        verbose_name = 'Platform Exchange'
        verbose_name_plural = 'Platform Exchanges'
    
        
class Sector(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True, default='not_set')
    platform_exchange = models.ForeignKey('PlatformExchange', on_delete=models.PROTECT)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "sector"
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectors'

class AssetSymbol(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    asset_full_name = models.CharField(max_length=100, null=True, blank=True)
    sector = models.ForeignKey('Sector', on_delete=models.PROTECT)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "asset_symbol"
        verbose_name = 'Asset Symbol'
        verbose_name_plural = 'Asset Symbols'

class DailyPrices(models.Model):
    
    class Kinds(models.TextChoices):
        BASE = 'B', 'base'
        FUTURES = 'F', 'futures contract'
        OPTIONS = 'O', 'options'

    symbol = models.ForeignKey('AssetSymbol', on_delete=models.PROTECT, default=None)
    session_date = models.DateField(unique=True)
    request_time = models.DateTimeField(unique=True, null=True, blank=True)
    price_day_open = models.FloatField(null=True, blank=True)
    price_day_high = models.FloatField(null=True, blank=True)
    price_day_low = models.FloatField(null=True, blank=True)
    price_day_close = models.FloatField(null=True, blank=True)
    day_volume = models.FloatField(null=True, blank=True)
    day_true_range = models.FloatField(null=True, blank=True)
    day_average_true_range = models.FloatField(null=True, blank=True)
    type_of_asset = models.CharField(max_length=1, choices=Kinds.choices, default=Kinds.BASE)

    class Meta:
        db_table = "daily_prices"
        verbose_name = 'Symbol Daily Prices (TR, ATR)'
        verbose_name_plural = 'Symbol Daily Prices (TR, ATR)'
        ordering = ['session_date']