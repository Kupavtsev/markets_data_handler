import django
django.setup()
from get_data.models import MP_Two_Hours, RealTimeData
from datetime import datetime, timedelta

from get_data.logic.psize import Position_Size

# lp last price
def work_with_last_price(symbol, session_date, lp):
    print('work_with_last_price')
    # YDS : str = (session_date-timedelta(days=1))
    session_date = datetime.strptime(session_date, "%Y-%m-%d")
    YDS : str = (session_date-timedelta(days=1)).strftime("%Y-%m-%d")
    mp_2h : isinstance = MP_Two_Hours.objects.get(symbol=symbol, session=YDS)
    body_size_ticks = mp_2h.body_size_ticks
    body_prc = mp_2h.body_size_percent
    # print('args: ', symbol, lp, body_prc)
    ps = Position_Size(symbol, lp, body_size_ticks, body_prc)
    ps_res = ps.pos_size()
    print(ps.symbol, 'lp: ', lp, ps_res)
    # save data to DB
    rt_data : isinstance = RealTimeData(
        symbol = ps.symbol,
        session = session_date,
        last_price = lp,
        futures_pos = ps_res[0],
        max_prc_stop = ps_res[1],
        amount_of_position = ps_res[2],
    )
    rt_data.save()