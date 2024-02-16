from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime

import numpy as np
import pandas as pd

from .tasks import check_response
from .binance_api import data_from_binance
from .models import AssetSymbol, DailyPrices

from .checker import cycle_of_response, asset_cycler

    
def index(request):
    if request.method == 'GET':  
        s = 'Quotes Data Handle'
        return HttpResponse(s, content_type='text/plain; charset=utf-8')
    else:
        return HttpResponse('Wrong method: 405')
    
def test(request):
    print('Func test!')
    check_response.delay()
    return HttpResponse('api request done')

def add_to_db(request):
    assets : list = AssetSymbol.objects.all()
    response : dict = data_from_binance(assets)

    # work with TR
    # response = {'ACHUSDT': [[1707436800000, '0.0182340', '0.0189570', '0.0182320', '0.0188610', '311960221', 1707523199999, '5815175.2732960', 70089, '146275523', '2727169.1899120', '0'], [1707523200000, '0.0188650', '0.0190400', '0.0184000', '0.0186680', '225214253', 1707609599999, '4211677.3072640', 57301, '112440056', '2103266.2089040', '0'], [1707609600000, '0.0186690', '0.0190300', '0.0184100', '0.0184990', '204383454', 1707695999999, '3833299.9845460', 50930, '97332304', '1825910.8149450', '0'], [1707696000000, '0.0184990', '0.0194260', '0.0181210', '0.0193350', '346107424', 1707782399999, '6463893.8764640', 87435, '163548586', '3052513.2204600', '0'], [1707782400000, '0.0193360', '0.0195310', '0.0187180', '0.0189990', '325356559', 1707868799999, '6241221.8233410', 86017, '142592272', '2737032.7255910', '0']], 'FETUSDT': [[1707436800000, '0.5593000', '0.6188000', '0.5569000', '0.6086000', '120998412', 1707523199999, '71889245.7464000', 353886, '58750794', '34891541.3728000', '0'], [1707523200000, '0.6086000', '0.6348000', '0.6008000', '0.6281000', '88518542', 1707609599999, '54793418.1794000', 279741, '44328109', '27445260.0303000', '0'], [1707609600000, '0.6281000', '0.6486000', '0.6219000', '0.6312000', '77848458', 1707695999999, '49446598.9975000', 250903, '36569264', '23232663.9894000', '0'], [1707696000000, '0.6313000', '0.6740000', '0.6217000', '0.6677000', '88585850', 1707782399999, '57352445.1929000', 309176, '42504687', '27554197.5026000', '0'], [1707782400000, '0.6677000', '0.6879000', '0.6498000', '0.6729000', '88639788', 1707868799999, '59418743.1388000', 334964, '42232156', '28321355.2890000', '0']]}
    

    # add to db
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

    x = cycle_of_response(response)
    tr_objects = DailyPrices.objects.filter(day_true_range=None)
    
    for object in tr_objects: 
        # print(object.session_date, object.symbol)
        for ses in x:
            for each in ses:
                # print(type(str(
                if str(object.symbol) == each[0] and str(object.session_date) == each[1]:
                    # print(True)
                    object.day_true_range = format(each[2], '.5f')
                    object.save()
            

    return HttpResponse('signs created from request...')


period = 14
#  sum / period
# Doesn't give me nessecary result yet.
def atr(request):
    asset_cycler()

    # assets : list = AssetSymbol.objects.all()
    # list_of_trs = []
    # for asset in assets:
    #     sessions = DailyPrices.objects.filter(symbol=asset)[1:15]
    #     for session in sessions:
    #         list_of_trs.append([str(asset), str(session.session_date), session.day_true_range])
    
    # print(list_of_trs)
    # print(len(list_of_trs))

    # df = pd.DataFrame(list_of_trs)
    # print(df)

    # for el in list_of_trs:
    #     for x in el:
            # print(x)

    return HttpResponse('atrs done')

# It doesn't correct!
def tr_total(request):
    # assets = AssetSymbol.objects.all()
    # for asset in assets:

    tr_objects = DailyPrices.objects.all().values()
    df = pd.DataFrame(list(tr_objects))
    print(df)

    # wrong method of calc!
    # for object in tr_objects:
    #     object.day_true_range = max(
    #         object.price_day_high-object.price_day_low,
    #         object.price_day_high-object.price_day_close,
    #         object.price_day_low-object.price_day_close)
    #     object.save()
    
    return HttpResponse('Total TRs calculated')