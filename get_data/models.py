from django.db import models
from django.contrib.postgres.fields import ArrayField



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
    class Kinds(models.TextChoices):
        BASE = 'S', 'spot'
        FUTURES = 'F', 'futures contract'
        OPTIONS = 'O', 'options'

    name = models.CharField(max_length=50, db_index=True)
    asset_full_name = models.CharField(max_length=100, null=True, blank=True)
    sector = models.ForeignKey('Sector', on_delete=models.PROTECT)
    type_of_asset = models.CharField(max_length=1, choices=Kinds.choices, default=Kinds.BASE)
    # capitalization/OI

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "asset_symbol"
        verbose_name = 'Asset Symbol'
        verbose_name_plural = 'Asset Symbols'

class DailyPrices(models.Model):
    
    symbol = models.ForeignKey('AssetSymbol', on_delete=models.PROTECT, default=None)
    session_date = models.DateField()
    request_time = models.DateTimeField(null=True, blank=True)
    price_day_open = models.FloatField(null=True, blank=True)
    price_day_high = models.FloatField(null=True, blank=True)
    price_day_low = models.FloatField(null=True, blank=True)
    price_day_close = models.FloatField(null=True, blank=True)
    day_volume = models.FloatField(null=True, blank=True)
    day_true_range = models.FloatField(null=True, blank=True)
    day_average_true_range = models.FloatField(null=True, blank=True)
    # 0:0.25 1:0.5 2:0.75 3:1 4:1.25 5:1.5 6:1.75 7:2 8:2.25 9:2.5 10:2.75 11:3 12:-0.25 13:-0.5 14/15/16/17/18/19/20/21/22/23
    atr_levels = ArrayField(base_field=models.FloatField(null=True, blank=True), default=list, null=True, blank=True, verbose_name='ATRs Levels')
    prev_two_ses_high_low = ArrayField(base_field=models.FloatField(null=True, blank=True), default=list, null=True, blank=True, verbose_name='H/L 2 Prev Ses')
    # prev_two_ses_low = None
    

    class Meta:
        db_table = "daily_prices"
        verbose_name = 'Daily (TR, ATR, ATR levs, 2SesHL)'
        verbose_name_plural = 'Daily (TR, ATR, ATR levs, 2SesHL)'
        ordering = ['symbol', '-session_date']
        unique_together = ('symbol', 'session_date')

class ATR(models.Model):
    symbol = models.CharField(max_length=50, db_index=True)
    session = models.DateField()
    Open = models.FloatField(null=True, blank=True)
    High = models.FloatField(null=True, blank=True)
    Low = models.FloatField(null=True, blank=True)
    Close = models.FloatField(null=True, blank=True)
    Volume = models.FloatField(null=True, blank=True)
    tr = models.FloatField(null=True, blank=True)
    atr = models.FloatField(null=True, blank=True)
    ma5 = models.FloatField(null=True, blank=True)
    ma10 = models.FloatField(null=True, blank=True)
    ma20 = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "atr"
        ordering = ['symbol', '-session']
        unique_together = ('symbol', 'session')


class Two_Hours(models.Model):
    symbol = models.ForeignKey('AssetSymbol', on_delete=models.PROTECT, default=None)
    session_date = models.DateField()
    start_of_candle = models.DateTimeField(null=True, blank=True)
    price_open = models.FloatField(null=True, blank=True)
    price_high = models.FloatField(null=True, blank=True)
    price_low = models.FloatField(null=True, blank=True)
    price_close = models.FloatField(null=True, blank=True)
    volume = models.FloatField(null=True, blank=True)
    

    class Meta:
        db_table = "two_hours_prices"
        verbose_name = 'Two Hours'
        verbose_name_plural = 'Two Hours'
        ordering = ['symbol', '-session_date']
        unique_together = ('symbol', 'start_of_candle')

class MP_Two_Hours(models.Model):
    symbol = models.CharField(max_length=20, db_index=True)
    session = models.DateField()
    top_tail = ArrayField(base_field=models.FloatField(null=True, blank=True), default=list, null=True, blank=True, verbose_name='top tail')
    top_tail_percent = models.FloatField(null=True, blank=True)
    body = ArrayField(base_field=models.FloatField(null=True, blank=True), default=list, null=True, blank=True, verbose_name='body')
    body_size_ticks = models.FloatField(null=True, blank=True)
    body_size_percent = models.FloatField(null=True, blank=True)
    bottom_tail = ArrayField(base_field=models.FloatField(null=True, blank=True), default=list, null=True, blank=True, verbose_name='bottom tail')
    bottom_tail_percent = models.FloatField(null=True, blank=True)
    periods_mp = ArrayField(base_field=models.IntegerField(null=True, blank=True), default=list, null=True, blank=True, verbose_name='visual market profile')
    periods_visualization = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = "mp_two_hours"
        verbose_name = 'MP Two Hours'
        verbose_name_plural = 'MP Two Hours'
        ordering = ['symbol', '-session']
        unique_together = ('symbol', 'session')


class RealTimeData(models.Model):
    symbol = models.CharField(max_length=20, db_index=True)
    session = models.DateField()
    request_time = models.DateTimeField(auto_now_add=True)
    last_price = models.FloatField(null=True, blank=True)
    futures_pos = models.FloatField(null=True, blank=True)
    max_prc_stop = models.FloatField(null=True, blank=True)
    amount_of_position = models.FloatField(null=True, blank=True)
    atr_prc_passed = models.IntegerField(null=True, blank=True, default=0)
    today_two_ses = models.BooleanField(null=True, blank=True, default=False)
    ysd_body_level = models.FloatField(null=True, blank=True, default=0)
    ysd_tail = models.FloatField(null=True, blank=True, default=0)
    ysd_body_border = models.FloatField(null=True, blank=True, default=0)
    atr_levels = ArrayField(base_field=models.FloatField(null=True, blank=True), default=list, null=True, blank=True)

    class Meta:
        db_table = "realtime_celery"
        verbose_name = 'RT Celery'
        verbose_name_plural = 'RT Celery'
        ordering = ['symbol', '-session']
        # unique_together = ('symbol', 'session')