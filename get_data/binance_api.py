import os
from binance import Client
# from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import datetime as dt
from datetime import datetime, timedelta
import asyncio
from concurrent.futures import ThreadPoolExecutor

from .checker import utcnow



'''
headers = ['Kline open time', 'Open price', 'High price', 'Low price', 'Close price', 'Volume', 'Kline Close time',
            'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Unused field, ignore']
'''
# Refactor to asyncio
def realtime(assets):
    f_klines = {}
    def check_binanceklines(
            asset,
            interval = Client.KLINE_INTERVAL_1MINUTE,
            limit = 5,      # minutes request
            end = int(dt.datetime.now(dt.timezone.utc).timestamp() * 1000)
        ):
        binance = Client()
        f_klines[asset.name] = binance.futures_klines(symbol=asset,interval=interval,endTime=end,limit=limit)

    with ThreadPoolExecutor() as executor:
        executor.map(check_binanceklines, assets)

    return f_klines

# def check_binanceklines(
#         symbol = 'BTCUSDT',
#         interval = Client.KLINE_INTERVAL_5MINUTE,
#         limit = 30,
#         end = int(dt.datetime.now(dt.timezone.utc).timestamp() * 1000)
#     ):
#     binance = Client()
#     return binance.futures_klines(symbol=symbol,interval=interval,endTime=end,limit=limit)



# SECRET INFO
# Connection with Binance API
def security() -> isinstance:
    print('security func')
    api_key = os.getenv("API")
    api_secret = os.getenv("Secret")
    client : isinstance = Client(api_key, api_secret)
    status : classmethod = client.get_system_status()
    print('status: ', status)
   
    return client

# Request Binance Data. Futures assets.
def data_from_binance(assets, request_days, interval) -> dict:
    print('data_from_binance func')
    # now = datetime.utcnow()
    now = utcnow()
    # dd/mm/YY H:M:S
    # dt_string : str = now.strftime("%Y-%m-%d")
    YDS : str = (datetime.utcnow()-timedelta(days=request_days)).strftime("%Y-%m-%d")
    client : isinstance = security()
    fh_klines : dict = {}

    def thread_test(asset):
        history : isinstance = client.futures_historical_klines(
            symbol=asset,
            interval=interval,  # can play with this e.g. '1h', '4h', '1w', etc.
            start_str=YDS,
            end_str=now
        )
        fh_klines[asset.name] = history

    with ThreadPoolExecutor() as executor:
        executor.map(thread_test, assets)

    return fh_klines

def real_time_data_binance(assets) -> dict:
    print('real_time_data_binance')
    client = security()
    f_klines = {}

    def request_thread(asset):
        realtime = client.futures_klines(
            symbol=asset,

        )
        f_klines[asset.name] = realtime

    with ThreadPoolExecutor() as executor:
        executor.map(request_thread, assets)

    return f_klines

# Syncron variant
# def data_from_binance(assets, request_days, interval) -> dict:
    # print('data_from_binance func')
    # now = datetime.utcnow()
    # # dd/mm/YY H:M:S
    # dt_string : str = now.strftime("%Y-%m-%d")
    # YDS : str = (datetime.utcnow()-timedelta(days=request_days)).strftime("%Y-%m-%d")
    # client : isinstance = security()
    # fh_klines : dict = {}
    # for asset in assets:
    #     history : isinstance = client.futures_historical_klines(
    #         symbol=asset,
    #         interval=interval,  # can play with this e.g. '1h', '4h', '1w', etc.
    #         start_str=YDS,
    #         end_str=dt_string
    #     )
    #     fh_klines[asset.name] = history

    # return fh_klines


# class Binance_data():
    print('Class:', __name__.Binance_data)
    client : isinstance = security()

    def binance_daily(assets, request_days) -> dict:
        print('method: ', __name__.data_from_binance)
        now = datetime.utcnow()
        dt_string : str = now.strftime("%Y-%m-%d")
        YDS : str = (datetime.utcnow()-timedelta(days=request_days)).strftime("%Y-%m-%d")
        client : isinstance = security()
        fh_klines : dict = {}
        for asset in assets:
            history : isinstance = client.futures_historical_klines(
                symbol=asset,
                interval='1d',  # can play with this e.g. '1h', '4h', '1w', etc.
                start_str=YDS,
                end_str=dt_string
            )
            fh_klines[asset.name] = history
        
        return fh_klines
    
    def binance_2h(assets, request_days) -> dict:
        print('method: ', __name__.data_from_binance)
        now = datetime.utcnow()
        dt_string : str = now.strftime("%Y-%m-%d")
        YDS : str = (datetime.utcnow()-timedelta(days=request_days)).strftime("%Y-%m-%d")
        client : isinstance = security()
        fh_klines : dict = {}
        for asset in assets:
            history : isinstance = client.futures_historical_klines(
                symbol=asset,
                interval='2h',  # can play with this e.g. '1h', '4h', '1w', etc.
                start_str=YDS,
                end_str=dt_string
            )
            fh_klines[asset.name] = history
        
        return fh_klines