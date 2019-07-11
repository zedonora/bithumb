from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import pybithumb
import time
import math
import base64
import hmac, hashlib
import urllib.parse
import pycurl
import json
from datetime import datetime
from urllib.request import Request, urlopen

# Create your models here.
@python_2_unicode_compatible
class Trade(models.Model):
    name = models.DecimalField(max_digits=6, decimal_places=2)
    mail = models.DecimalField(max_digits=6, decimal_places=2)
    age = models.IntegerField(default=0)
    opening_price = models.DecimalField(max_digits=6, decimal_places=2)
    closing_price = models.DecimalField(max_digits=6, decimal_places=2)
    min_price = models.DecimalField(max_digits=6, decimal_places=2)
    max_price = models.DecimalField(max_digits=6, decimal_places=2)
    average_price = models.DecimalField(max_digits=6, decimal_places=2)
    units_traded = models.DecimalField(max_digits=6, decimal_places=2)
    volume_1day = models.DecimalField(max_digits=6, decimal_places=2)
    volume_7day = models.DecimalField(max_digits=6, decimal_places=2)
    buy_price = models.DecimalField(max_digits=6, decimal_places=2)
    sell_price = models.DecimalField(max_digits=6, decimal_places=2)
    fluctate_24h = models.DecimalField(max_digits=6, decimal_places=2)
    fluctate_rate_24h = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField(auto_now=False, auto_now_add=False)

@python_2_unicode_compatible
class XCoinAPI(models.Model):
    api_url = "https://api.bithumb.com";
    api_key = "";
    api_secret = "";

    def __init__(self, api_key, api_secret):
        self.api_key = api_key;
        self.api_secret = api_secret;

    def body_callback(self, buf):
        self.contents = buf;

    def microtime(self, get_as_float = False):
        if get_as_float:
            return time.time()
        else:
            return '%f %d' % math.modf(time.time())

    def usecTime(self) :
        mt = self.microtime(False)
        mt_array = mt.split(" ")[:2];
        return mt_array[1] + mt_array[0][2:5];

    def xcoinApiCall(self, endpoint, rgParams):
        # 1. Api-Sign and Api-Nonce information generation.
        # 2. Request related information from the Bithumb API server.
        #
        # - nonce: it is an arbitrary number that may only be used once.
        # - api_sign: API signature information created in various combinations values.

        endpoint_item_array = {
            "endpoint" : endpoint
        };

        uri_array = dict(endpoint_item_array, **rgParams); # Concatenate the two arrays.

        str_data = urllib.parse.urlencode(uri_array);

        nonce = self.usecTime();

        data = endpoint + chr(0) + str_data + chr(0) + nonce;
        utf8_data = data.encode('utf-8');

        key = self.api_secret;
        utf8_key = key.encode('utf-8');

        h = hmac.new(bytes(utf8_key), utf8_data, hashlib.sha512);
        hex_output = h.hexdigest();
        utf8_hex_output = hex_output.encode('utf-8');

        api_sign = base64.b64encode(utf8_hex_output);
        utf8_api_sign = api_sign.decode('utf-8');


        curl_handle = pycurl.Curl();
        curl_handle.setopt(pycurl.POST, 1);
        #curl_handle.setopt(pycurl.VERBOSE, 1); # vervose mode :: 1 => True, 0 => False
        curl_handle.setopt(pycurl.POSTFIELDS, str_data);

        url = self.api_url + endpoint;
        curl_handle.setopt(curl_handle.URL, url);
        curl_handle.setopt(curl_handle.HTTPHEADER, ['Api-Key: ' + self.api_key, 'Api-Sign: ' + utf8_api_sign, 'Api-Nonce: ' + nonce]);
        curl_handle.setopt(curl_handle.WRITEFUNCTION, self.body_callback);
        curl_handle.perform();

        #response_code = curl_handle.getinfo(pycurl.RESPONSE_CODE); # Get http response status code.

        curl_handle.close();

        return (json.loads(self.contents));

@python_2_unicode_compatible
class Ticker(models.Model):

    def get_market_detail(self):
        #detail = pybithumb.get_orderbook("ALL")
        detail = pybithumb.get_orderbook("ETH")
        ms = int(detail["timestamp"])
        dt = datetime.fromtimestamp(ms/1000)
        timestampStr = dt.strftime("%Y-%m-%d (%H:%M:%S)")
        detail["timestamp"] = timestampStr
        detail["bids"] = detail["bids"][2]
        detail["asks"] = detail["asks"][2]

        #return detail
        return (json.loads(json.dumps(detail)))

#https://hatpub.tistory.com/38 Bithmb(0), Upbit, Poloniex(O), Bitmex, Bittrex, Kraken, Coinbase
@python_2_unicode_compatible
class Bithumb(models.Model):

    def get_ticker_info(self):
        urlTicker = urllib.request.urlopen('https://api.bithumb.com/public/ticker/ETH')
        #urlTicker = urllib.request.urlopen('https://api.bithumb.com/public/ticker/all')
        readTicker = urlTicker.read()
        jsonTicker = json.loads(readTicker)
        ms = int(jsonTicker['data']["date"])
        dt = datetime.fromtimestamp(ms / 1000)
        timestampStr = dt.strftime("%Y-%m-%d (%H:%M:%S)")
        jsonTicker['data']["date"] = timestampStr
        return jsonTicker

@python_2_unicode_compatible
class UpBit(models.Model):

    def get_ticker_info(self):
        #urlTicker = urllib.request.urlopen('https://api.upbit.com/v1/ticker?markets/all')
        urlTicker = urllib.request.urlopen('https://api.upbit.com/v1/ticker?markets=KRW-ETH')
        readTicker = urlTicker.read()
        jsonTicker = json.loads(readTicker)[0]
        ms = int(jsonTicker["timestamp"])
        dt = datetime.fromtimestamp(ms / 1000)
        timestampStr = dt.strftime("%Y-%m-%d (%H:%M:%S)")
        jsonTicker['timestamp'] = timestampStr
        return jsonTicker

@python_2_unicode_compatible
class Coinone(models.Model):

    def get_ticker_info(self):
        urlTicker = urllib.request.urlopen('https://api.coinone.co.kr/ticker/?currency=eth')
        #urlTicker = urllib.request.urlopen('https://api.coinone.co.kr/ticker/?currency=all')
        readTicker = urlTicker.read()
        jsonTicker = json.loads(readTicker)
        ms = int(jsonTicker["timestamp"])
        dt = datetime.fromtimestamp(ms / 1000)
        timestampStr = dt.strftime("%Y-%m-%d (%H:%M:%S)")
        jsonTicker['timestamp'] = timestampStr
        return jsonTicker

@python_2_unicode_compatible
class Poloniex(models.Model):
    def get_ticker_info(self):
        urlTicker = urllib.request.urlopen('https://poloniex.com/public?command=returnTicker')
        readTicker = urlTicker.read()
        jsonTicker = json.loads(readTicker)
        jsonTicker = jsonTicker['USDT_ETH']
        return jsonTicker

@python_2_unicode_compatible
class Bitmex(models.Model):
    def get_ticker_info(self):
        reqBTC = Request('https://www.bitmex.com/api/v1/orderBook/L2?symbol=ETH&depth=25' , headers={'User-Agent': 'Mozilla/5.0'})
        readBTC = urlopen(reqBTC).read()
        jsonBTC = json.loads(readBTC)
        FindBTC = jsonBTC['last']
        BTC = int(FindBTC)
        urlTicker = urllib.request.urlopen('https://www.bitmex.com/api/v1/orderBook/L2?symbol=ETH&depth=25')
        readTicker = urlTicker.read()
        jsonTicker = json.loads(readTicker)
        FindETC = jsonTicker['etc']['last']
        ETC = int(FindETC)
        FindBTC = jsonTicker['btc']['last']
        BTC = int(FindBTC)
        FindETH = jsonTicker['eth']['last']
        ETH = int(FindETH)
        FindXRP = jsonTicker['xrp']['last']
        XRP = int(FindXRP)

@python_2_unicode_compatible
class Bittrex(models.Model):
    def get_ticker_info(self):
        urlTicker = urllib.request.urlopen('https://api.bittrex.com/api/v1.1/public/getmarketsummary?market=usd-eth')
        readTicker = urlTicker.read()
        jsonTicker = json.loads(readTicker)
        jsonTicker = jsonTicker['result']
        return jsonTicker

@python_2_unicode_compatible
class Kraken(models.Model):
    def get_ticker_info(self):
        urlTicker = urllib.request.urlopen('https://api.kraken.com/0/public/Ticker?pair=ETHUSD')
        readTicker = urlTicker.read()
        jsonTicker = json.loads(readTicker)['result']['XETHZUSD']
        return jsonTicker

@python_2_unicode_compatible
class Coinbase(models.Model):
    def get_ticker_info(self):
        reqBTC = Request('https://api.coinbase.com/v2/prices/BTC-USD/spot' , headers={'User-Agent': 'Mozilla/5.0'})
        readBTC = urlopen(reqBTC).read()
        jsonBTC = json.loads(readBTC)
        FindBTC = jsonBTC['last']
        urlTicker = urllib.request.urlopen('https://api.coinbase.com/v2/prices/BTC-USD/spot')
        readTicker = urlTicker.read()
        jsonTicker = json.loads(readTicker)
        FindETC = jsonTicker['etc']['last']
        ETC = int(FindETC)
        FindBTC = jsonTicker['btc']['last']
        BTC = int(FindBTC)
        FindETH = jsonTicker['eth']['last']
        ETH = int(FindETH)
        FindXRP = jsonTicker['xrp']['last']
        XRP = int(FindXRP)
