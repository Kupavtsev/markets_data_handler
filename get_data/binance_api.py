import os
from binance import Client
# from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from datetime import datetime, timedelta
import asyncio



'''
headers = ['Kline open time', 'Open price', 'High price', 'Low price', 'Close price', 'Volume', 'Kline Close time',
            'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Unused field, ignore']
'''

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
    now = datetime.utcnow()
    # dd/mm/YY H:M:S
    dt_string : str = now.strftime("%Y-%m-%d")
    YDS : str = (datetime.utcnow()-timedelta(days=request_days)).strftime("%Y-%m-%d")
    client : isinstance = security()
    fh_klines : dict = {}
    for asset in assets:
        history : isinstance = client.futures_historical_klines(
            symbol=asset,
            interval=interval,  # can play with this e.g. '1h', '4h', '1w', etc.
            start_str=YDS,
            end_str=dt_string
        )
        fh_klines[asset.name] = history

    


    return fh_klines


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