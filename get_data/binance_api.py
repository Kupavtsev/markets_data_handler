import os
# import dotenv
from binance import Client
# from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
# import pandas as pd
from datetime import datetime, timedelta


'''
headers = ['Kline open time', 'Open price', 'High price', 'Low price', 'Close price', 'Volume', 'Kline Close time',
            'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Unused field, ignore']
'''

# SECRET INFO
# Connection with Binance API
def security():
    # dotenv.load_dotenv()
    api_key = os.getenv("API")
    api_secret = os.getenv("Secret")

    client = Client(api_key, api_secret)
    status = client.get_system_status()
    print(api_key)
    print(status)
    return client

# Request Binance Data. Futures assets.
def data_from_binance(assets):
   
    # datetime object containing current date and time
    now = datetime.utcnow()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y-%m-%d")
    YDS = (datetime.utcnow()-timedelta(days=1)).strftime("%Y-%m-%d")
    print(YDS)
    print("date and time =", dt_string)

    client = security()
    history_data = []
    for asset in assets:
        history = client.futures_historical_klines(
            symbol=asset,
            interval='1d',  # can play with this e.g. '1h', '4h', '1w', etc.
            start_str=YDS,
            end_str=dt_string
        )
        history_data.append(history)
    return history_data

security()