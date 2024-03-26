from rest_framework import serializers
from .models import ATR, RealTimeData

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

class RealTimeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealTimeData
        fields = (
            'symbol',
            'session',
            'request_time',
            'last_price',
            'futures_pos',
            'max_prc_stop',
            'amount_of_position',
            'atr_prc_passed',
            'today_two_ses'
        )