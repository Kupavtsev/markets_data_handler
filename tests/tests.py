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