import numpy as np
import pandas as pd
from datetime import datetime
from django.utils import timezone

from .models import ATR, AssetSymbol, DailyPrices

today = datetime.utcnow()
today_string = today.strftime("%Y-%m-%d")

# example of response
# RESPONSE = {'ACHUSDT': [[1707436800000, '0.0182340', '0.0189570', '0.0182320', '0.0188610', '311960221', 1707523199999, '5815175.2732960', 70089, '146275523', '2727169.1899120', '0'], [1707523200000, '0.0188650', '0.0190400', '0.0184000', '0.0186680', '225214253', 1707609599999, '4211677.3072640', 57301, '112440056', '2103266.2089040', '0'], [1707609600000, '0.0186690', '0.0190300', '0.0184100', '0.0184990', '204383454', 1707695999999, '3833299.9845460', 50930, '97332304', '1825910.8149450', '0'], [1707696000000, '0.0184990', '0.0194260', '0.0181210', '0.0193350', '346107424', 1707782399999, '6463893.8764640', 87435, '163548586', '3052513.2204600', '0'], [1707782400000, '0.0193360', '0.0195310', '0.0187180', '0.0189990', '325356559', 1707868799999, '6241221.8233410', 86017, '142592272', '2737032.7255910', '0']], 'FETUSDT': [[1707436800000, '0.5593000', '0.6188000', '0.5569000', '0.6086000', '120998412', 1707523199999, '71889245.7464000', 353886, '58750794', '34891541.3728000', '0'], [1707523200000, '0.6086000', '0.6348000', '0.6008000', '0.6281000', '88518542', 1707609599999, '54793418.1794000', 279741, '44328109', '27445260.0303000', '0'], [1707609600000, '0.6281000', '0.6486000', '0.6219000', '0.6312000', '77848458', 1707695999999, '49446598.9975000', 250903, '36569264', '23232663.9894000', '0'], [1707696000000, '0.6313000', '0.6740000', '0.6217000', '0.6677000', '88585850', 1707782399999, '57352445.1929000', 309176, '42504687', '27554197.5026000', '0'], [1707782400000, '0.6677000', '0.6879000', '0.6498000', '0.6729000', '88639788', 1707868799999, '59418743.1388000', 334964, '42232156', '28321355.2890000', '0']]}

# df = pd.DataFrame(RESPONSE)
# assets_list = df.columns
# number_of_assets = len(df.columns)


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
    object.day_average_true_range = format(atr/14, '.5f')
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

# Wrong method, missing sessions
# def atr_total(asset):
#     sessions = DailyPrices.objects.filter(symbol=asset).filter(day_average_true_range=None)
#     if len(sessions) > 15:
#         print('you can calc')
#         atr = 0
#         for session in sessions[1:15]:
#             atr += session.day_true_range
#         object = sessions[0]
#         object.day_average_true_range = format(atr/14, '.5f')
#         object.save()
#             # print(session.symbol, session.session_date, session.day_true_range, \
#             #        type(session.day_true_range), session.day_average_true_range)
#         atr_total(asset)    
#     else: print('not enaugh data')


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

    model_instances = []
    for row in df.iterrows():
        data = row[1].to_dict()
        # print(data)
        model_instance = ATR(**data)
        model_instances.append(model_instance)

    # print(model_instances)
    ATR.objects.bulk_create(model_instances)
