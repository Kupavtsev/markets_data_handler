# import json
import django
from django.http import HttpResponse
django.setup()
from get_data.models import MP_Two_Hours, RealTimeData, AssetSymbol, DailyPrices
from datetime import datetime, timedelta

from get_data.logic.psize import Position_Size

arred = lambda x,n : x*(10**n)//1/(10**n)

# All this functions make async or thread from work_with_last_price
def atr_moves(last_price, price_open, atr):
    ticks_from_the_open = last_price - price_open
    # price_movemnt_by_atr_in_percent = (ticks_from_the_open / price_open)*100
    atr_price_movement_in_percent = int(ticks_from_the_open/atr*100)
    return atr_price_movement_in_percent

def two_ses_position(last_price, today_two_ses):
    if last_price >= today_two_ses[0] or last_price <= today_two_ses[1]:
        relative_position = True        # higher
    # elif last_price <= today_two_ses[1]:
    #     relative_position = None        # lower
    else:
        relative_position = False        # inside
    return relative_position

def ysd_body(lp, today_open, body_size_ticks, top_tail, body, bottom_tail):
    if lp > today_open:
        ysd_body_level = arred((today_open + body_size_ticks), 6)
        ysd_body_border = arred((body[1] + body_size_ticks), 6)
        ysd_tail = arred((top_tail[1] + body_size_ticks), 6)
    else: 
        ysd_body_level = arred((today_open - body_size_ticks), 6)
        ysd_body_border = arred((body[0] - body_size_ticks), 6)
        ysd_tail = arred((bottom_tail[0] - body_size_ticks), 6)

    return (ysd_body_level, ysd_tail, ysd_body_border)

# lp last price
def work_with_last_price(symbol, session_date, lp):
    print('work_with_last_price')
    # YDS : str = (session_date-timedelta(days=1))
    session_date = datetime.strptime(session_date, "%Y-%m-%d")
    YSD : str = (session_date-timedelta(days=1)).strftime("%Y-%m-%d")
    # Today Data
    asset : str = AssetSymbol.objects.get(name=symbol)
    today_data = DailyPrices.objects.get(symbol=asset, session_date=session_date)
    today_open = today_data.price_day_open
    today_atr = today_data.day_average_true_range
    today_atr_levels = today_data.atr_levels
    # today_two_ses = today_data.prev_two_ses_high_low
    today_two_ses = two_ses_position(lp, today_data.prev_two_ses_high_low)
    atr_prc_passed = atr_moves(lp, today_open, today_atr)
    # Yesterday data
    mp_2h : isinstance = MP_Two_Hours.objects.get(symbol=symbol, session=YSD)
    body_size_ticks = mp_2h.body_size_ticks
    body_prc = mp_2h.body_size_percent
    top_tail = mp_2h.top_tail
    body = mp_2h.body
    bottom_tail = mp_2h.bottom_tail
    # print('args: ', symbol, lp, body_prc)

    # logic
    # if lp > today_open:
    #     ysd_body_level = today_open + body_size_ticks
    # else: ysd_body_level = today_open - body_size_ticks
    ysd_body_level = ysd_body(lp, today_open, body_size_ticks, top_tail, body, bottom_tail)
    ps = Position_Size(symbol, lp, body_size_ticks, body_prc, today_atr)
    ps_res = ps.pos_size()
    print(f'{ps.symbol}, "lp: {lp}", {ps_res[2]}')
    
    # save data to DB
    rt_data : isinstance = RealTimeData(
        symbol = ps.symbol,
        session = session_date,
        last_price = lp,
        futures_pos = ps_res[0],
        max_prc_stop = ps_res[1],
        amount_of_position = ps_res[2],
        atr_prc_passed=atr_prc_passed,
        today_two_ses=today_two_ses,
        ysd_body_level=ysd_body_level[0],
        ysd_tail = ysd_body_level[1],
        ysd_body_border = ysd_body_level[2],
    )
    if not RealTimeData.objects.filter(symbol=symbol):
        rt_data.save()
    else:
        RealTimeData.objects.filter(symbol=symbol).update(
            session = session_date,
            last_price = lp,
            futures_pos = ps_res[0],
            max_prc_stop = ps_res[1],
            amount_of_position = ps_res[2],
            atr_prc_passed = atr_prc_passed,
            today_two_ses=today_two_ses,
            ysd_body_level=ysd_body_level[0],
            ysd_tail = ysd_body_level[1],
            ysd_body_border = ysd_body_level[2],
        )

    # Real Time API
    # LP_DATA['symbol'] = ps.symbol
    # LP_DATA['session'] = session_date
    # LP_DATA['last_price'] = lp
    # LP_DATA['futures_pos'] = ps_res[0]
    # LP_DATA['max_prc_stop'] = ps_res[1]
    # LP_DATA['amount_of_position'] = ps_res[2]