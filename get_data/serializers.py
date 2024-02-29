from rest_framework import serializers
from .models import ATR, AssetSymbol, DailyPrices

class ATRSerializer(serializers.ModelSerializer):

    class Meta:
        model = ATR
        fields = (
            'symbol',
            'session',
            'Open',
            'High',
            'Low',
            'Close',
            'Volume',
            'atr',
        )