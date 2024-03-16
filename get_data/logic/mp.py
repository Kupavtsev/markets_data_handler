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

# or I shoul pass this data to Class ? Or create sub functions
def mp_calc(hl):
    h = hl[0]
    l = hl[1]
    print(h, l, hl[2], hl[3])

# Not useful possably !!!
def hl_2h_list(symbol, session_data, **data):
    db_2h_ohlc = Two_Hours.objects.filter(symbol=symbol, session_date=session_data)
    for hl in db_2h_ohlc:
        mp_calc([hl.price_high, hl.price_low])
    #     print(each2h.symbol, each2h.session_date, each2h.start_of_candle, each2h.price_close)
    # periods_mp = data['periods_mp']
    # print(periods_mp)

def prepair_mp2h(ses):
    # runs through each symbol session
    periods = 40
    symbol = ses.symbol
    session_data = ses.session_date
    high = ses.price_day_high
    low = ses.price_day_low
    close = ses.price_day_close
    atr = ATR.objects.get(symbol=ses.symbol, session=ses.session_date).atr
    # Logic. This DATA for ONE session!
    step_price_prc = atr/close*100
    step_prc = step_price_prc/periods
    step_ticks = close*step_prc/100
    price_range = high - low
    len_periods = price_range / step_ticks

    periods_in_ticks = np.arange(low, high+step_ticks, step_ticks)
    periods_mp = [0]*len(periods_in_ticks)
   
    data = {'periods_in_ticks': periods_in_ticks, 'periods_mp': periods_mp}
    # hl_2h_list(symbol, session_data, **data)
    db_2h_ohlc = Two_Hours.objects.filter(symbol=symbol, session_date=session_data)
    for hl in db_2h_ohlc:
        mp_calc([hl.price_high, hl.price_low, hl.start_of_candle, hl.session_date])
    

# Basic. work well 3
def main():
    start = time.time()
    assets : list = AssetSymbol.objects.all()
    # It runs every session by asset
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