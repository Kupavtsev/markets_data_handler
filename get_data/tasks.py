from celery import shared_task
from .binance_api import data_from_binance
from .models import AssetSymbol, DailyPrices
import json, io

@shared_task(bind=True)
def check_response(self):
    assets = AssetSymbol.objects.all()
    # print('Asets from task: ', assets)
    response = data_from_binance(assets)
    # print('response: ', response)
    # save data to DB

    # print(response["ACHUSDT"][0][0])
    # print(response["ACHUSDT"][0][1])
    
    # Below experiments... Above Done!

    type_check = AssetSymbol.objects.get(name="ACHUSDT")
    print('type_check: ', type_check, ' ', type(type_check))

    for data_name in response.keys():
        print('data_name: ', data_name, ' ', type(data_name))

        new_session = DailyPrices(
            symbol=DailyPrices.objects.filter(symbol=data_name),
            # symbol=AssetSymbol.objects.filter(name="ACHUSDT"),
            session_date=response[data_name][0][0],
            request_time=response[data_name][0][0],
            price_day_open=response[data_name][0][1],
            price_day_high=response[data_name][0][2],
            price_day_low=response[data_name][0][3],
            price_day_close=response[data_name][0][4],
            day_volume=response[data_name][0][5],
        )
        
        # import io, json 
        with io.open('data_dict.json', 'a', encoding='utf-8') as f: 
            f.write(json.dumps(new_session, indent=1, ensure_ascii=False))
        
        new_session.save()
        
    return "done"