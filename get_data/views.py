from django.http import HttpResponse

from .tasks import check_response

from django.utils import timezone
from datetime import datetime
from .binance_api import data_from_binance
from .models import AssetSymbol, DailyPrices

    
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
    
    for data_name in response.keys():

        asset : str = AssetSymbol.objects.get(name=data_name)
        session_date = datetime.fromtimestamp(response[data_name][0][0]/1000).strftime("%Y-%m-%d")
        response_data : list = response[data_name][0]

        new_session : isinstance = DailyPrices(
            session_date=session_date,
            request_time=timezone.now(),
            price_day_open=response_data[1],
            price_day_high=response_data[2],
            price_day_low=response_data[3],
            price_day_close=response_data[4],
            day_volume=response_data[5],
        )
        new_session.symbol : str = asset
        # This is work with first requested Symbol, so it won't work with todays added New symbols.
        if not DailyPrices.objects.filter(symbol=asset, session_date=session_date):
            new_session.save()

    return HttpResponse('signs created from request...')