import datetime as dt

from binance.client import Client


def check_binanceklines(
        symbol = 'BTCUSDT',
        interval = Client.KLINE_INTERVAL_5MINUTE,
        limit = 30,
        end = int(dt.datetime.now(dt.timezone.utc).timestamp() * 1000)
    ):
    binance = Client()
    return binance.futures_klines(symbol=symbol,interval=interval,endTime=end,limit=limit)


if __name__ == '__main__':
    klines = check_binanceklines()

    # Print len, the first and last elemnt of returned klines list.
    print(f'Length of the returned klines list: {len(klines)}')
    print(type(klines))
    # print(klines[-1])
    print('close =>',klines[-1][4])

    # for line in klines:
    #     print(line)

    3.2082525,3.307705,3.4071575,3.5066100000000002,3.6060625,3.705515,3.8049675,3.90442,4.0038725,4.103325,4.2027775,4.30223,
    3.0093475,2.909895,2.8104425,2.71099,2.6115375,2.512085,2.4126325,2.31318,2.2137275,2.114275,2.0148225,1.9153700000000002