import websocket as wb

BINANCE_SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
ws = wb.WebSocketApp("")


def on_open(ws):
    ws.send("{'event':'addChannel','channel':'ethusdt@kline_1m'}")
    print("connected")


def on_message(ws, message):
    print(message)


ws.run_forever()
