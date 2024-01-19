from django.contrib import admin
from .models import PlatformExchange, Sector, AssetSymbol, DailyPrices


class DailyPricesAdmin(admin.ModelAdmin):
    list_display = ('session_date', 'symbol', 'price_day_close', 'day_average_true_range')
    list_display_links = ('symbol',)
    search_fields = ('symbol', 'session_date')


admin.site.register(DailyPrices, DailyPricesAdmin)
admin.site.register(Sector)
admin.site.register(PlatformExchange)
admin.site.register(AssetSymbol)