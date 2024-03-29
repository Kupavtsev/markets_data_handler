# from django.db.models import Q
import json
from django.http import HttpResponse
# from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


import time


from get_data.serializers import ATRSerializer, RealTimeDataSerializer
# from datetime import datetime

# import numpy as np
# import pandas as pd

from .tasks import check_response
from .binance_api import data_from_binance, real_time_data_binance
from .models import AssetSymbol, ATR, RealTimeData, \
                    DailyPrices, Two_Hours, MP_Two_Hours

from .checker import response_to_db, atr_calc_for_last_session, \
            trs_save_to_db, response_2h_to_db
from get_data.logic.mp import main
    
def index(request):
    if request.method == 'GET':  
        assets : list = AssetSymbol.objects.all()
        last_date = DailyPrices.objects.first().session_date
        last_2h = Two_Hours.objects.first().session_date
        last_atr_date = ATR.objects.first().session
        last_2hmp_date = MP_Two_Hours.objects.first().session
        # for asset in assets:
        #     print(asset.sector, asset.name)
        
        return render(
            request,
            'get_data/index.html',
                {
                'assets':assets,
                'last_date':last_date,
                'last_2h':last_2h,
                'last_atr_date': last_atr_date,
                'last_2hmp_date': last_2hmp_date
                }
            )
    else:
        return HttpResponse('Wrong method: 405')
    
def test(request):
    print('Func test!')
    check_response.delay()
    return HttpResponse('api request done')

def calc_2h_mp(request):
    print('calc_2h_mp')
    main()
    return HttpResponse('calc_2h_mp')

def test_request(request):
    assets : list = AssetSymbol.objects.all()
    request_days = 4
    start = time.time()
    try:
        response : dict = real_time_data_binance(assets)
    except Exception:
        print(Exception)
        response = {}
    print('response: ', type(response), len(response))
    print('response: ', response)
    end = time.time()
    time_taken_req =  end - start
    print('time_taken: ', end - start)
    return HttpResponse(f'Test request done. Request take {time_taken_req}')

# In Celery and do it every 2H. No this is historical data
def two_hours_to_db(request):
    assets : list = AssetSymbol.objects.all()
    request_days = 4
    start = time.time()
    try:
        response : dict = data_from_binance(assets, request_days, interval='2h')
    except Exception:
        print(Exception)
        response = {}
    # print('response: ', type(response), len(response))
    # print('response: ', response)
    end = time.time()
    time_taken_req =  end - start
    print('time_taken: ', end - start)
    # 4.5 one day with 3 elements. Sync
    # 1.5-3.5 the same with threading
    if len(response)>0:
        start = time.time()
        response_2h_to_db(response)
        end = time.time()
        time_taken_db =  end - start    # 3-4.75 one day with 3 elements. Sync
    return HttpResponse(f'2H request done. Request take {time_taken_req}. Add to DB take {time_taken_db}')

# This function request the data, add this data to DB, calc TRs from this data and again add it to DB sessions
def add_to_db(request):
    assets : list = AssetSymbol.objects.all()
    request_days = 15
    start = time.time()
    try:
        response : dict = data_from_binance(assets, request_days, interval='1d')
    except Exception:
        print(Exception)
        # send alert
        # create delay
        # print(ConnectionError)
        response = {}
    end = time.time()
    time_taken_req =  end - start
    print('response: ', type(response), len(response))
    # print(response)
    print('time_taken: ', time_taken_req)

    # example of response
    # response = {'ACHUSDT': [[1707436800000, '0.0182340', '0.0189570', '0.0182320', '0.0188610', '311960221', 1707523199999, '5815175.2732960', 70089, '146275523', '2727169.1899120', '0'], [1707523200000, '0.0188650', '0.0190400', '0.0184000', '0.0186680', '225214253', 1707609599999, '4211677.3072640', 57301, '112440056', '2103266.2089040', '0'], [1707609600000, '0.0186690', '0.0190300', '0.0184100', '0.0184990', '204383454', 1707695999999, '3833299.9845460', 50930, '97332304', '1825910.8149450', '0'], [1707696000000, '0.0184990', '0.0194260', '0.0181210', '0.0193350', '346107424', 1707782399999, '6463893.8764640', 87435, '163548586', '3052513.2204600', '0'], [1707782400000, '0.0193360', '0.0195310', '0.0187180', '0.0189990', '325356559', 1707868799999, '6241221.8233410', 86017, '142592272', '2737032.7255910', '0']], 'FETUSDT': [[1707436800000, '0.5593000', '0.6188000', '0.5569000', '0.6086000', '120998412', 1707523199999, '71889245.7464000', 353886, '58750794', '34891541.3728000', '0'], [1707523200000, '0.6086000', '0.6348000', '0.6008000', '0.6281000', '88518542', 1707609599999, '54793418.1794000', 279741, '44328109', '27445260.0303000', '0'], [1707609600000, '0.6281000', '0.6486000', '0.6219000', '0.6312000', '77848458', 1707695999999, '49446598.9975000', 250903, '36569264', '23232663.9894000', '0'], [1707696000000, '0.6313000', '0.6740000', '0.6217000', '0.6677000', '88585850', 1707782399999, '57352445.1929000', 309176, '42504687', '27554197.5026000', '0'], [1707782400000, '0.6677000', '0.6879000', '0.6498000', '0.6729000', '88639788', 1707868799999, '59418743.1388000', 334964, '42232156', '28321355.2890000', '0']]}
    # response time 3.38-4.2 for 10 days and 3 elements. Synchronic
    # 2.78-3 with threading
    
    # Realise it with Class and Methods, response would be atr of Class inst
    if len(response) > 0:       # > 0 ?
        start = time.time()
        response_to_db(response)
        trs_save_to_db(response)
        # atr, atrs levels, 2ses levels for today
        atr_calc_for_last_session('atr_today')
        end = time.time()
        time_taken_db =  end - start    # 5.3 for 10 days and 3 elements. Synchronic
    # elif response != None:
    else:
        print('no response')

    return HttpResponse(f'Days, ATR & levels for today, 2 ses H/L, Request take {time_taken_req}. Add to DB take {time_taken_db}')
    # return HttpResponseRedirect(reverse('get_data:index'))

def atr(request):
    print('Start to calc all ATRs from DB')
    atr_calc_for_last_session('atr_total')
    return HttpResponse('atrs...')

# API REST
# last_prices=[
#     {
#         "symbol": "ACHUSDT",
#         "session": "2024-03-25",
#         "request_time": "2024-03-24T18:20:03.328469Z",
#         "last_price": 0.043466,
#         "futures_pos": 939.040319,
#         "max_prc_stop": 12.45,
#         "amount_of_position": 40.8163
#     },] 
# def get_ajax_data(request=None):
#     last_prices     
#     # last_prices = 0.45
#     if request is None:
#         return last_prices
#     else:
#         return HttpResponse(json.dumps(last_prices), content_type='application/json')

@api_view(['GET', 'POST'])
def ohlc_atr(request):
    if request.method == 'GET':
        data = ATR.objects.all()
        serializer = ATRSerializer(data, many=True)
        return Response(serializer.data)
    
@api_view(['GET', 'POST'])
def rt_data(request):
    if request.method == 'GET':
        data = RealTimeData.objects.all()
        serializer = RealTimeDataSerializer(data, many=True)
        return Response(serializer.data)