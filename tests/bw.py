import websocket, json
import rel

cc = 'btcusdt'
interval = '1m'
socket = f'wss://stream.binance.com:9443/ws/{cc}@kline_{interval}'

ws = websocket

closes, highs, lows = [], [], []

def on_message(ws, message):
    # print(message)
    json_message = json.loads(message)
    candle = json_message['k']
    is_candle_closed = candle['x']
    close = candle['c']
    high = candle['h']
    low = candle['l']
    vol = candle['v']

    if is_candle_closed:
        closes.append(float(close))
        highs.append(float(high))
        lows.append(float(low))

    print(closes)
    print(highs)
    print(lows)

    # print(close)
    # print(high)
    # print(low)
    # print(vol)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

ws = websocket.WebSocketApp(socket, on_message=on_message, on_close=on_close)
ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
rel.dispatch()
# print(ws)