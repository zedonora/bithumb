from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import os
import urllib.request
import pybithumb
import time
import math
import base64
import hmac, hashlib
import urllib.parse
import pycurl
import json

from django.shortcuts import render
from . import models, serializers

# Create your views here.

class GetTrade(APIView):

    def get(self, request, format=None):

        last_five = models.Trade.objects.all().order_by()[:5]

        serializer = serializers.TradeSerializer(last_five, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

class GetXcoin(APIView):

    def get(self, request, format=None):

        # API 값 가져오기
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        json_data = os.path.join(BASE_DIR, 'bitthumb/.config_secret/settings_key.json')
        config_file = json.loads(open(json_data).read())
        #api_key = config_file['BITHUMB']['API_KEY'] or ""
        #api_secret = config_file['BITHUMB']['API_SECRET'] or ""
        api_key = ""
        api_secret = ""
        api = models.XCoinAPI(api_key, api_secret)
        rgParams = json.loads(open(os.path.join(BASE_DIR, 'trade/params.json')).read())
        result = api.xcoinApiCall("/public/ticker", rgParams)

        print("status: " + result["status"])
        print("last: " + result["data"]["closing_price"])
        print("sell: " + result["data"]["sell_price"])
        print("buy: " + result["data"]["buy_price"])

        return render(request, 'search.html', context=result)

class GetTicker(APIView):

    def get(self, request, format=None):

        api = models.Ticker
        result = api.get_market_detail(self)
        print(result)
        # print("status: " + result["status"])
        # print("last: " + result["data"]["closing_price"])
        # print("sell: " + result["data"]["sell_price"])
        # print("buy: " + result["data"]["buy_price"])

        #Response(status=status.HTTP_200_OK)
        return render(request, 'ticker.html', context=result)


