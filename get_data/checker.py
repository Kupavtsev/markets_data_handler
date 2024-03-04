import numpy as np
import pandas as pd
from datetime import datetime
from django.utils import timezone
import websocket, json

from .models import ATR, AssetSymbol, DailyPrices

today = datetime.utcnow()
today_string = today.strftime("%Y-%m-%d")

# **************************************************
# Websocket part
# cc = 'btcusdt'
# interval = '1s'
# socket = f'wss://stream.binance.com:9443/ws/{cc}@kline_{interval}'

# ws = websocket

# def on_message(ws, message):
#     print(message)

# def on_close(ws, close_status_code, close_msg):
#     print("### closed ###")

# ws = websocket.WebSocketApp(socket, on_message=on_message, on_close=on_close)
# ws.run_forever()
# print(ws)

# **************************************************



def response_to_db(response):
    for symbol, lists_of_days in response.items():
        for each_date in lists_of_days:

            asset : str = AssetSymbol.objects.get(name=symbol)
            session_date = datetime.fromtimestamp(each_date[0]/1000).strftime("%Y-%m-%d")   #date

            new_session : isinstance = DailyPrices(
                session_date=session_date,
                request_time=timezone.now(),
                price_day_open=each_date[1],
                price_day_high=each_date[2],
                price_day_low=each_date[3],
                price_day_close=each_date[4],
                day_volume=each_date[5],
            )
            new_session.symbol = asset
            # This is work with first requested Symbol, so it won't work with todays added New symbols.
            if not DailyPrices.objects.filter(symbol=asset, session_date=session_date):
                new_session.save()

# TR by asset for last session of response list
def tr(df):
    result = []
    for el in df.columns:
        number_of_session = len(df[el])
        price_day_high = float(df[el][number_of_session-1][2])
        price_day_low = float(df[el][number_of_session-1][3])
        price_day_close_prev = float(df[el][number_of_session-2][4])
        tr = max((price_day_high - price_day_low), (price_day_high - price_day_close_prev), (price_day_close_prev - price_day_low))
        session_date = datetime.fromtimestamp(df[el][number_of_session-1][0]/1000).strftime("%Y-%m-%d")   #date
        if session_date != today_string:
            result.append([el, session_date, tr])
    
    return result       # List of Lists (asset, timestamp, TR)
        
# cycle of deleting last element to calculate TRs
def cycle_of_response(respone):
    df = pd.DataFrame(respone)
    result = []
    for session in range(len(df)-1):
        res = tr(df)
        # print(res)
        result.append(res)
        df = df[:-1]

    return result

def trs_save_to_db(response):
    x = cycle_of_response(response)
    tr_objects = DailyPrices.objects.filter(day_true_range=None)    # get sessions without TRs
    # Add to sessions from DB TRs wich has calculated from response
    for object in tr_objects:       
        for ses in x:
            for each in ses:
                if str(object.symbol) == each[0] and str(object.session_date) == each[1]:
                    object.day_true_range = format(each[2], '.5f')
                    object.save()

# ATR calculator for today
def atr_calc(asset):
    sessions = DailyPrices.objects.filter(symbol=asset)
    atr = 0
    for session in sessions[1:15]:
        atr += session.day_true_range 
    object = sessions[0]
    today_atr = format(atr/14, '.5f')
    object.day_average_true_range = today_atr
    # atr levels for today: open + today_atr 
    count = float(today_atr)*0.25
    start = count  # you need to change start on every cycle
    atr_levels = []
    for i in range(12):     # for plus atr move
        res = object.price_day_open + start
        atr_levels.append(res)
        start += count
    start = count
    for i in range(12):     # for minus atr move
        res = object.price_day_open - start
        atr_levels.append(res)
        start += count
    object.atr_levels = atr_levels
    object.save()
    
def atr_calc_for_last_session(switcher):
    assets : list = AssetSymbol.objects.all()
    # assets = ['ACHUSDT', 'FETUSDT']
    if switcher == 'atr_today':
        for asset in assets:
            atr_calc(asset.id)
    elif switcher == 'atr_total':
        for asset in assets:
            atr_total_calc_once2(asset.id)

def atr_total_calc_once(asset):
    # sessions = DailyPrices.objects.filter(symbol=asset)
    sessions = DailyPrices.objects.filter(symbol=asset, day_average_true_range=None)
    sessions2 = ATR.objects.filter(symbol=asset)
    # sessions2 = ATR.objects.all()

    try:
        count = len(sessions)
        # count = 18
        while count > 10:
        # if len(sessions) > 15:
            # print('you can calc')
            atr = 0
            for session in sessions[1:15]:
                # print('session =>', session.symbol, session.session_date, session.day_average_true_range)
                atr += session.day_true_range
            object = sessions[0]
            object.day_average_true_range = format(atr/14, '.5f')
            print('ATR object =>', object.symbol, object.session_date, object.day_average_true_range)

            object2 = ATR(
                symbol = session.symbol,
                session_date = object.session_date,
                day_average_true_range = object.day_average_true_range
            )
            object2.session_date = sessions[0].session_date
            # object2.day_average_true_range = format(atr/14, '.5f')
            print('object2: ', object2.day_average_true_range)
            # object.save()
            # if not object2.session_date:
            #     object2.save()
            count -= 1
            print(count)
            # atr_total_calc_once(asset)
    except Exception as e: print(e)
    finally: print('finished')

    # for el in range(len(sessions)):
    #     atr_total_calc_once(asset)
# Find the session without ATR, and work with it! Cycling...
    
def atr_total_calc_once2(asset):
    sessions = DailyPrices.objects.filter(symbol=asset)
    ses_list = []
    for ses in sessions:
        ses_dict = {}
        ses_dict['symbol'] = str(ses.symbol)
        ses_dict['session'] = str(ses.session_date)
        ses_dict['Open'] = ses.price_day_open
        ses_dict['High'] = ses.price_day_high
        ses_dict['Low'] = ses.price_day_low
        ses_dict['Close'] = ses.price_day_close
        ses_dict['Volume'] = ses.day_volume
        ses_dict['tr'] = 0
        ses_dict['atr'] = 0
        ses_list.append(ses_dict)
    df = pd.DataFrame(ses_list)
    # print(df)
    df = df.sort_index(ascending=False)
    # print('*'*9, 'after')
    period = 14
    tr1 = abs(df['High'] - df['Low'])
    tr2 = abs(df['High'] - df['Close'].shift(1))
    tr3 = abs(df['Low'] - df['Close'].shift(1))
    ranges = pd.concat([tr1, tr2, tr3], axis=1)
    tr = ranges.max(axis=1)
    df['tr'] = tr
    atr_all = tr.shift(1).rolling(period).sum()/period
    df['atr'] = round(atr_all, 6)
    # print(df)
    
    # NaN not accepted by JSON Serializers
    df = df.fillna(0)
    
    model_instances = []
    for row in df.iterrows():
        data = row[1].to_dict()
        # print(data)
        model_instance = ATR(**data)
        model_instances.append(model_instance)

    # print(model_instances)
    ATR.objects.bulk_create(
        model_instances,
        update_conflicts=True,
        # unique_fields=['symbol', 'session', 'Open', 'High', 'Low', 'Close', 'tr'],
        unique_fields=['symbol', 'session'],
        update_fields=['atr'],
        )
