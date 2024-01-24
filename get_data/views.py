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
            new_session.symbol : str = asset
            # This is work with first requested Symbol, so it won't work with todays added New symbols.
            if not DailyPrices.objects.filter(symbol=asset, session_date=session_date):
                new_session.save()

    return HttpResponse('signs created from request...')

# Max(H-L, H-Cp, L-Cp)
def tr_total(request):
    # assets = AssetSymbol.objects.all()
    # for asset in assets:


    tr_objects = DailyPrices.objects.all()
    for object in tr_objects:
        # symbol = object.symbol
        # sd = object.session_date
        # prev_day_close = object.price_day_close()
        # print(symbol, ' ', sd)
        object.day_true_range = max(
            object.price_day_high-object.price_day_low,
            object.price_day_high-object.price_day_close,
            object.price_day_low-object.price_day_close)
        object.save()
    
    return HttpResponse('Total TRs calculated')