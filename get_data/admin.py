from django.contrib import admin
from .models import PlatformExchange, Sector, AssetSymbol, DailyPrices, ATR, Two_Hours


class DailyPricesAdmin(admin.ModelAdmin):
    list_display = ('session_date', 'symbol', 'price_day_close', 'day_true_range', 'day_average_true_range')
    list_display_links = ('symbol',)
    search_fields = ('symbol', 'session_date')

class ATRsAdmin(admin.ModelAdmin):
    list_display = ('session', 'symbol', 'atr')
    list_display_links = ('symbol',)

class Two_HoursAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'session_date','start_of_candle')
    list_display_links = ('symbol', 'session_date')


admin.site.register(DailyPrices, DailyPricesAdmin)
admin.site.register(ATR, ATRsAdmin)
admin.site.register(Two_Hours, Two_HoursAdmin)
admin.site.register(Sector)
admin.site.register(PlatformExchange)
admin.site.register(AssetSymbol)