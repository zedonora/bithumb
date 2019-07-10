from rest_framework import serializers
from . import models

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Trade
        fields = (
            'id',
            'name',
            'mail',
            'age',
            'opening_price',
            'closing_price',
            'min_price',
            'max_price',
            'average_price',
            'units_traded',
            'volume_1day',
            'volume_7day',
            'buy_price',
            'sell_price',
            'fluctate_24h',
            'fluctate_rate_24h',
            'date',
        )

class XcoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.XCoinAPI
        fields = (
            '__all__'
        )

class TickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ticker
        fields = (
            '__all__'
        )