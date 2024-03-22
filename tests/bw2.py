# https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md
import time
import websocket, json
import rel

cc = 'btcusdt'
cc2 = 'achusdt'

interval = '1m'
socket2 = f'wss://fstream.binance.com/stream?streams={cc}@kline_{interval}/{cc2}@kline_{interval}'
# socket_test = f'wss://stream.binance.com:9443/stream?streams=bnbusdt@kline_1m/btcusdt@depth@100ms'
# socket_fut = f'wss://fstream.binance.com/ws/{cc}@kline_{interval}'    # one asset
# wss://dstream.binancefuture.com/
# wss://data-stream.binance.vision:443/ws/btcusdt@kline_1m
ws = websocket

opens, highs, lows, closes = [], [], [], []

def on_message(ws, message):
    # print(message)
    json_message = json.loads(message)
    candle = json_message['data']['k']
    symbol = candle['s']
    is_candle_closed = candle['x']
    open = candle['o']
    high = candle['h']
    low = candle['l']
    close = candle['c']
    vol = candle['v']

    if is_candle_closed:
        opens.append(float(open))
        highs.append(float(high))
        lows.append(float(low))
        closes.append(float(close))

    print(symbol, '=>')
    print('opens: ', closes)
    print('highs: ', highs)
    print('lows: ', lows)
    print('closes: ', closes)

    # print(symbol, '=> ',close)
    # print(symbol, '=> ', open, high, low, close)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_error(ws, error):
    print('error: ', error)

ws = websocket.WebSocketApp(socket2, on_message=on_message, on_close=on_close, on_error=on_error)
ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
rel.dispatch()
# print(ws)