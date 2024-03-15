# import multiprocessing
# from multiprocessing import Process, Pool
import time
import numpy as np

import django
django.setup()
from get_data.models import DailyPrices, AssetSymbol, Two_Hours, ATR
# from get_data.checker import utcnow
from datetime import date, timedelta

startdate = date.today()
enddate = startdate - timedelta(days=6)


def mp_2h(symbol, session_data, **data):
    data_2h_from_db = Two_Hours.objects.filter(symbol=symbol, session_date=session_data)
    # for each2h in data_2h_from_db:
    #     print(each2h.symbol, each2h.session_date, each2h.start_of_candle, each2h.price_close)
    periods_mp = data['periods_mp']
    print(periods_mp)

def prepair_mp2h(ses):
    # runs through each symbol session
    # Inside this loop should be all logic and saving data to db
    periods = 40
    symbol = ses.symbol
    session_data = ses.session_date
    high = ses.price_day_high
    low = ses.price_day_low
    close = ses.price_day_close
    atr = ATR.objects.get(symbol=ses.symbol, session=ses.session_date).atr
    # Logic
    step_price_prc = atr/close*100
    step_prc = step_price_prc/periods
    step_ticks = close*step_prc/100
    price_range = high - low
    len_periods = price_range / step_ticks
    # print(symbol, session_data, step_price_prc, step_prc, step_ticks, len_periods)


    periods_tick_steps = np.arange(low, high+step_ticks, step_ticks)
    periods_mp = [0]*len(periods_tick_steps)
    # print(symbol, session_data, len(periods_tick_steps), len(periods_mp), high, periods_tick_steps[-1])
    # next
    data = {'periods_tick_steps': periods_tick_steps, 'periods_mp': periods_mp}
    mp_2h(symbol, session_data, **data)
    # get very sign from this new model and add data from ATR.
    # than from 2H
    # and each time its new loops, or funcs, or funcs inside funcs!
    

# Basic. work well 3
def main():
    start = time.time()
    assets : list = AssetSymbol.objects.all()
    def func_sessions(asset):
        sessions = DailyPrices.objects.filter(symbol=asset, session_date__range=[enddate, startdate])          # get last 7 sessions
        for ses in sessions:
            prepair_mp2h(ses)
    for asset in assets:
        func_sessions(asset)
    end = time.time()
    time_taken =  end - start
    print(time_taken)   #2.2 ; 4.3/3.47

# Work well 2
# def main():
#     start = time.time()
#     pool = Pool(processes=4)
#     assets : list = AssetSymbol.objects.all()
#     pool.map(prepair_mp2h, assets)
#     end = time.time()
#     time_taken =  end - start
#     print(time_taken)   # 3.4


# v2
# def multiprocess_prepair():
    
#     assets : list = AssetSymbol.objects.all()
#     procs = []
#     # initiating process with arguments
#     def func_sessions(asset):
#         sessions = DailyPrices.objects.filter(symbol=asset, session_date__range=[enddate, startdate])          # get last 7 sessions
#         for ses in sessions:
#             proc = Process(target=prepair_mp2h, args=(ses,))
#             procs.append(proc)
#             proc.start()
#     for asset in assets:
#         func_sessions(asset)
        

#     for proc in procs:
#         proc.join()

# def main():
#     start = time.time()
#     multiprocess_prepair()
#     end = time.time()
#     time_taken =  end - start
#     print('time_taken: ', time_taken)   # 20s


# Work well 1 first V
# def multiprocess_prepair():
    
#     assets : list = AssetSymbol.objects.all()
#     procs = []
#     # initiating process with arguments
#     for asset in assets:
#         proc = Process(target=prepair_mp2h, args=(asset,))
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