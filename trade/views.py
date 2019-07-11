from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import os
import json

from django.http import JsonResponse
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
        # Bithumb - ETH
        api = models.Bithumb
        raw_data = api.get_ticker_info(self)
        print(raw_data)
        index = 1
        row = {}
        row['id'] = index
        row['name'] = 'Bithumb'
        row['ticker'] = raw_data['data']['opening_price']
        row['timestamp'] = raw_data['data']['date']
        row['bidsprice'] = raw_data['data']['buy_price']
        row['bidquantity'] = raw_data['data']['units_traded']
        row['asksprice'] = raw_data['data']['sell_price']
        row['asksquantity'] = raw_data['data']['24H_fluctate']
        return_list = []
        return_list.append(row.copy())

        # UpBit - ETH
        api = models.UpBit
        raw_data = api.get_ticker_info(self)
        index = index + 1
        row['id'] = index
        row['name'] = 'UpBit'
        row['ticker'] = raw_data['trade_price']
        row['timestamp'] = raw_data['timestamp']
        row['bidsprice'] = raw_data['change_price']
        row['bidquantity'] = raw_data['change_rate']
        row['asksprice'] = raw_data['signed_change_price']
        row['asksquantity'] = raw_data['signed_change_rate']

        return_list.append(row.copy())

        # CoinOne - ETH
        api = models.Coinone
        raw_data = api.get_ticker_info(self)
        index = index + 1
        row['id'] = index
        row['name'] = 'CoinOne'
        row['ticker'] = raw_data['last']
        row['timestamp'] = row['timestamp']
        #row['timestamp'] = raw_data['timestamp']
        row['bidsprice'] = raw_data['high']
        row['bidquantity'] = raw_data['volume']
        row['asksprice'] = raw_data['low']
        row['asksquantity'] = raw_data['volume']

        return_list.append(row.copy())

        # Poloniex - ETH
        api = models.Poloniex
        raw_data = api.get_ticker_info(self)
        index = index + 1
        row['id'] = index
        row['name'] = 'Poloniex'
        row['ticker'] = raw_data['last']
        row['timestamp'] = row['timestamp']
        #row['timestamp'] = raw_data['timestamp']
        row['bidsprice'] = raw_data['highestBid']
        row['bidquantity'] = raw_data['baseVolume']
        row['asksprice'] = raw_data['lowestAsk']
        row['asksquantity'] = raw_data['quoteVolume']

        return_list.append(row.copy())

        # Bittrex - ETH
        api = models.Bittrex
        raw_data = api.get_ticker_info(self)[0]
        index = index + 1
        row['id'] = index
        row['name'] = 'Bittrex'
        row['ticker'] = raw_data['Last']
        row['timestamp'] = row['timestamp']
        #row['timestamp'] = raw_data['timestamp']
        row['bidsprice'] = raw_data['Bid']
        row['bidquantity'] = raw_data['BaseVolume']
        row['asksprice'] = raw_data['Ask']
        row['asksquantity'] = raw_data['BaseVolume']

        return_list.append(row.copy())

        # Kraken - ETH
        api = models.Kraken
        raw_data = api.get_ticker_info(self)
        index = index + 1
        row['id'] = index
        row['name'] = 'Kraken'
        row['ticker'] = raw_data['c'][0]
        row['timestamp'] = row['timestamp']
        #row['timestamp'] = raw_data['timestamp']
        row['bidsprice'] = raw_data['b'][0]
        row['bidquantity'] = raw_data['b'][2]
        row['asksprice'] = raw_data['a'][0]
        row['asksquantity'] = raw_data['a'][2]

        return_list.append(row.copy())

        return_list = sorted(return_list, key=lambda k: k['id'])

        return_json = {}
        return_json['data'] = return_list
        print(return_json)
        return_json = json.loads(json.dumps(return_json))
        #Response(status=status.HTTP_200_OK)
        return render(request, 'ticker.html', context=return_json)

class GetAjaxTicker(APIView):

    def get(self, request, format=None):
        # Bithumb - ETH
        api = models.Bithumb
        raw_data = api.get_ticker_info(self)
        print(raw_data)
        index = 1
        row = {}
        row['id'] = index
        row['name'] = 'Bithumb'
        row['ticker'] = raw_data['data']['opening_price']
        row['timestamp'] = raw_data['data']['date']
        row['bidsprice'] = raw_data['data']['buy_price']
        row['bidquantity'] = raw_data['data']['units_traded']
        row['asksprice'] = raw_data['data']['sell_price']
        row['asksquantity'] = raw_data['data']['24H_fluctate']
        return_list = []
        return_list.append(row.copy())

        # UpBit - ETH
        api = models.UpBit
        raw_data = api.get_ticker_info(self)
        index = index + 1
        row['id'] = index
        row['name'] = 'UpBit'
        row['ticker'] = raw_data['trade_price']
        row['timestamp'] = raw_data['timestamp']
        row['bidsprice'] = raw_data['change_price']
        row['bidquantity'] = raw_data['change_rate']
        row['asksprice'] = raw_data['signed_change_price']
        row['asksquantity'] = raw_data['signed_change_rate']

        return_list.append(row.copy())

        # CoinOne - ETH
        api = models.Coinone
        raw_data = api.get_ticker_info(self)
        index = index + 1
        row['id'] = index
        row['name'] = 'CoinOne'
        row['ticker'] = raw_data['last']
        row['timestamp'] = row['timestamp']
        # row['timestamp'] = raw_data['timestamp']
        row['bidsprice'] = raw_data['high']
        row['bidquantity'] = raw_data['volume']
        row['asksprice'] = raw_data['low']
        row['asksquantity'] = raw_data['volume']

        return_list.append(row.copy())

        # Poloniex - ETH
        api = models.Poloniex
        raw_data = api.get_ticker_info(self)
        index = index + 1
        row['id'] = index
        row['name'] = 'Poloniex'
        row['ticker'] = raw_data['last']
        row['timestamp'] = row['timestamp']
        # row['timestamp'] = raw_data['timestamp']
        row['bidsprice'] = raw_data['highestBid']
        row['bidquantity'] = raw_data['baseVolume']
        row['asksprice'] = raw_data['lowestAsk']
        row['asksquantity'] = raw_data['quoteVolume']

        return_list.append(row.copy())

        # Bittrex - ETH
        api = models.Bittrex
        raw_data = api.get_ticker_info(self)[0]
        index = index + 1
        row['id'] = index
        row['name'] = 'Bittrex'
        row['ticker'] = raw_data['Last']
        row['timestamp'] = row['timestamp']
        # row['timestamp'] = raw_data['timestamp']
        row['bidsprice'] = raw_data['Bid']
        row['bidquantity'] = raw_data['BaseVolume']
        row['asksprice'] = raw_data['Ask']
        row['asksquantity'] = raw_data['BaseVolume']

        return_list.append(row.copy())

        # Kraken - ETH
        api = models.Kraken
        raw_data = api.get_ticker_info(self)
        index = index + 1
        row['id'] = index
        row['name'] = 'Kraken'
        row['ticker'] = raw_data['c'][0]
        row['timestamp'] = row['timestamp']
        # row['timestamp'] = raw_data['timestamp']
        row['bidsprice'] = raw_data['b'][0]
        row['bidquantity'] = raw_data['b'][2]
        row['asksprice'] = raw_data['a'][0]
        row['asksquantity'] = raw_data['a'][2]

        return_list.append(row.copy())

        return_list = sorted(return_list, key=lambda k: k['id'])

        return_json = {}
        return_json['data'] = return_list
        return JsonResponse(return_list, safe=False)
