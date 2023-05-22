import json
import pandas as pd
import uuid
import requests
import datetime as dt
import bybit


class Token:
    def __init__(self, obj):
        self.symbol = obj.symbol
        self.open_time = obj.open_time
        self.open = obj.open
        self.high = obj.high
        self.low = obj.low
        self.close = obj.close
        self.volume = obj.volume
        self.turnover = obj.turnover


class Info:
    def __init__(self, obj):
        self.symbol = obj.get('symbol'),
        self.bid_price = obj.get('bid_price'),
        self.ask_price = obj.get('ask_price'),
        self.last_price = obj.get('last_price'),
        self.last_tick_direction = obj.get('last_tick_direction'),
        self.prev_price_24h = obj.get('prev_price_24h'),
        self.price_24h_pcnt = obj.get('price_24h_pcnt'),
        self.high_price_24h = obj.get('high_price_24h'),
        self.low_price_24h = obj.get('low_price_24h'),
        self.prev_price_1h = obj.get('prev_price_1h'),
        self.mark_price = obj.get('mark_price'),
        self.index_price = obj.get('index_price'),
        self.open_interest = obj.get('open_interest'),
        self.countdown_hour = obj.get('countdown_hour'),
        self.turnover_24h = obj.get('turnover_24h'),
        self.volume_24h = obj.get('volume_24h'),
        self.funding_rate = obj.get('funding_rate'),
        self.predicted_funding_rate = obj.get('predicted_funding_rate'),
        self.next_funding_time = obj.get('next_funding_time'),
        self.predicted_delivery_price = obj.get('predicted_delivery_price'),
        self.total_turnover = obj.get('total_turnover'),
        self.total_volume = obj.get('total_volume'),
        self.delivery_fee_rate = obj.get('delivery_fee_rate'),
        self.delivery_time = obj.get('delivery_time'),
        self.price_1h_pcnt = obj.get('price_1h_pcnt'),
        self.open_value = obj.get('open_value')


class User:
    def __init__(self, cfg) -> None:
        self.id = str(uuid.uuid4())
        self.api_key = cfg.api_key
        self.api_secret = cfg.api_secret


class Client:
    def __init__(self) -> None:
        self.is_connected = False
        self.client = None
        self.info = None
        self.kline_list = None

    def logIn_client(self, api_key, api_secret):
        self.client = bybit.bybit(test=False, api_key=api_key,
                                  api_secret=api_secret)
        self.is_connected = True

    def get_info(self, symbol):
        result = self.client.Market.Market_symbolInfo(symbol=symbol).result()
        self.info = Info(result[0]['result'][0])

        df = pd.DataFrame(vars(self.info))
        df.to_csv("data/info.csv", index=False)

    def get_kline_list(self, symbol, interval, startTime, endTime):
        url = "https://api.bybit.com/v2/public/kline/list"

        startTime = str(int(startTime.timestamp()))
        endTime = str(int(endTime.timestamp()))

        req_params = {"symbol": symbol, 'interval': interval,
                      'from': startTime, 'to': endTime}

        df = pd.DataFrame(json.loads(requests.get(
            url, params=req_params).text)['result'])

        if (len(df.index) == 0):
            return None

        df.index = [dt.datetime.fromtimestamp(x) for x in df.open_time]
        df.to_csv(f'data/{symbol}.csv')

    def read_kline_data(self, symbol):
        try:
            print(pd.read_csv(f'data/{symbol}.csv', index_col=[0]))
        except:
            pass
