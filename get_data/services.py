
from datetime import datetime, timedelta

from .models import AssetSymbol, DailyPrices

# now = datetime.utcnow()
# dt_string : str = now.strftime("%Y-%m-%d")


# Max(H-L, H-Cp, L-Cp)
def tr_total():
    DailyPrices.objects.filter()
    tr_objects = DailyPrices.objects.all()
    for object in tr_objects:
        object.day_true_range = max(
            object.price_day_high-object.price_day_low,
            object.price_day_high-object.price_day_close,
            object.price_day_low-object.price_day_close)
        object.save
    
    return 'done'


class Atr():

    


    def tr_calc(data):
        print('tr_calc')
        data = [list(x) for x in data]          # list of tuples to list of lists
        '''
        data - from database
        tr - el[-1]
        high - el[3]
        low - el[4]
        prev_close - data[count][5]
        '''
        tr_list = []
        count = 0

        for el in data[1:]:
            if el[-2] == None:
                print('IF statment has started...')
                # Max(H-L, H-Cp, L-Cp)
                trs = max(el[3]-el[4], el[3]-data[count][5], el[4]-data[count][5])
                trs = format(trs, '.4f')
                id = el[0]
                count += 1
                tr_list.append(trs)
        
        return tr_list