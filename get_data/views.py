# from django.db.models import Q
from django.http import HttpResponse
# from django.utils import timezone
# from datetime import datetime

# import numpy as np
# import pandas as pd

from .tasks import check_response
from .binance_api import data_from_binance
from .models import AssetSymbol

from .checker import response_to_db, atr_calc_for_last_session, trs_save_to_db

    
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

# This function request the data, add this data to DB, calc TRs from this data and again add it to DB sessions
def add_to_db(request):
    assets : list = AssetSymbol.objects.all()
    request_days = 20
    try:
        response : dict = data_from_binance(assets, request_days)
    except Exception:
        print(Exception)
        # send alert
        # create delay
        # print(ConnectionError)
        response = {}
    print('response: ', type(response), len(response))

    # example of response
    # response = {'ACHUSDT': [[1707436800000, '0.0182340', '0.0189570', '0.0182320', '0.0188610', '311960221', 1707523199999, '5815175.2732960', 70089, '146275523', '2727169.1899120', '0'], [1707523200000, '0.0188650', '0.0190400', '0.0184000', '0.0186680', '225214253', 1707609599999, '4211677.3072640', 57301, '112440056', '2103266.2089040', '0'], [1707609600000, '0.0186690', '0.0190300', '0.0184100', '0.0184990', '204383454', 1707695999999, '3833299.9845460', 50930, '97332304', '1825910.8149450', '0'], [1707696000000, '0.0184990', '0.0194260', '0.0181210', '0.0193350', '346107424', 1707782399999, '6463893.8764640', 87435, '163548586', '3052513.2204600', '0'], [1707782400000, '0.0193360', '0.0195310', '0.0187180', '0.0189990', '325356559', 1707868799999, '6241221.8233410', 86017, '142592272', '2737032.7255910', '0']], 'FETUSDT': [[1707436800000, '0.5593000', '0.6188000', '0.5569000', '0.6086000', '120998412', 1707523199999, '71889245.7464000', 353886, '58750794', '34891541.3728000', '0'], [1707523200000, '0.6086000', '0.6348000', '0.6008000', '0.6281000', '88518542', 1707609599999, '54793418.1794000', 279741, '44328109', '27445260.0303000', '0'], [1707609600000, '0.6281000', '0.6486000', '0.6219000', '0.6312000', '77848458', 1707695999999, '49446598.9975000', 250903, '36569264', '23232663.9894000', '0'], [1707696000000, '0.6313000', '0.6740000', '0.6217000', '0.6677000', '88585850', 1707782399999, '57352445.1929000', 309176, '42504687', '27554197.5026000', '0'], [1707782400000, '0.6677000', '0.6879000', '0.6498000', '0.6729000', '88639788', 1707868799999, '59418743.1388000', 334964, '42232156', '28321355.2890000', '0']]}
    
    # Realise it with Class and Methods, response would be atr of Class inst
    if len(response) > 1:
        response_to_db(response)
        trs_save_to_db(response)
        # need check if empty bd
        atr_calc_for_last_session('atr_today')
        
    # elif response != None:
    else:
        print('no response')

    return HttpResponse('signs created from request...')


def atr(request):
    atr_calc_for_last_session('atr_total')
    return HttpResponse('atrs...')