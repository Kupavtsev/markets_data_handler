from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse

from .tasks import check_response

from django.utils import timezone
from datetime import datetime
from .binance_api import data_from_binance
from .models import AssetSymbol, DailyPrices

    
def index(request):
    
    # assets = AssetSymbol.objects.all()
    # print('Asets from task: ', assets)

    if request.method == 'GET':  
        s = 'Binance Data Handler\r\n\r\n\r\n'
        return HttpResponse(s, content_type='text/plain; charset=utf-8')
    else:
        return HttpResponse('Wrong method: 405')
    
def test(request):
    print('Func test!')
    check_response.delay()
    return HttpResponse('api request done')

def add_to_db(request):
    assets = AssetSymbol.objects.all()
    # print('Asets from task: ', assets)
    response = data_from_binance(assets)
    # print('response: ', response)
    # save data to DB

    
    # Below experiments... Above Done!


    for data_name in response.keys():
        asset = AssetSymbol.objects.get(name=data_name)
        # print('asset: ', asset, ' ', type(asset))
        new_session = DailyPrices(
            session_date=datetime.fromtimestamp(response[data_name][0][0]/1000).strftime("%Y-%m-%d"),
            request_time=timezone.now(),
            price_day_open=response[data_name][0][1],
            price_day_high=response[data_name][0][2],
            price_day_low=response[data_name][0][3],
            price_day_close=response[data_name][0][4],
            day_volume=response[data_name][0][5],
        )
        # print('new_session: ', new_session)
        new_session.symbol = asset
        # print('new_session with asset: ', new_session)

        # This is work with first requested Symbol, so it won't work with todays added New symbols.
        if not DailyPrices.objects.filter(symbol=asset, session_date=datetime.fromtimestamp(response[data_name][0][0]/1000).strftime("%Y-%m-%d")):
            new_session.save()
        return HttpResponse('the date is actual...')

    return HttpResponse('signs created from request...')