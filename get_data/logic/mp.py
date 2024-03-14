import multiprocessing
from multiprocessing import Process, Pool
import time

import django
django.setup()
from get_data.models import DailyPrices, AssetSymbol, Two_Hours, ATR
# from get_data.checker import utcnow
from datetime import date, timedelta

startdate = date.today()
enddate = startdate - timedelta(days=6)


def prepair_2hmp(asset):
    sessions = DailyPrices.objects.filter(symbol=asset, session_date__range=[enddate, startdate])          # get last 7 sessions
    print(asset, sessions[0])
    # runs through each symbol session
    # Inside this loop should be all logic and saving data to db
    periods = 40
    for ses in sessions:
        # print(ses.symbol, ses.session_date)
        symbol = ses.symbol
        session_data = ses.session_date
        high = ses.price_day_high
        low = ses.price_day_low
        close = ses.price_day_close
        atr = ATR.objects.get(symbol=ses.symbol, session=ses.session_date).atr
        # print(symbol, session_data, atr)
        # Logic
        step_price_prc = atr/close*100
        step_prc = step_price_prc/periods
        step_ticks = close*step_prc/100
        range = high - low
        len_periods = range / step_ticks
        print(symbol, session_data, step_price_prc, step_prc, step_ticks, len_periods)

    # next
    # get very sign from this new model and add data from ATR.
    # than from 2H
    # and each time its new loops, or funcs, or funcs inside funcs!
    

# Basic. work well 3
def main():
    start = time.time()
    assets : list = AssetSymbol.objects.all()
    for asset in assets:
        prepair_2hmp(asset)
    end = time.time()
    time_taken =  end - start
    print(time_taken)   #2.2

# Work well 2
# def main():
#     start = time.time()
#     pool = Pool(processes=4)
#     assets : list = AssetSymbol.objects.all()
#     pool.map(prepair_2hmp, assets)
#     end = time.time()
#     time_taken =  end - start
#     print(time_taken)   # 3.4


# Work well 1
# def multiprocess_prepair():
    
#     assets : list = AssetSymbol.objects.all()
#     procs = []
#     # initiating process with arguments
#     for asset in assets:
#         proc = Process(target=prepair_2hmp, args=(asset,))
#         procs.append(proc)
#         proc.start()
#     for proc in procs:
#         proc.join()

# def main():
#     start = time.time()
#     multiprocess_prepair()
#     end = time.time()
#     time_taken =  end - start
#     print(time_taken)   # 2.8
    
# Check with threading, async and Celery!