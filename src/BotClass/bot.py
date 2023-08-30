import math
from tradingview_ta import TA_Handler, Interval
import datetime


class MultiCoin:
    def __init__(self):
        ''' 
        params - interval: 
                    INTERVAL_1_MINUTE = "1m"
                    INTERVAL_5_MINUTES = "5m"
                    INTERVAL_15_MINUTES = "15m"
                    INTERVAL_30_MINUTES = "30m"
                    INTERVAL_1_HOUR = "1h"
                    INTERVAL_2_HOURS = "2h"
                    INTERVAL_4_HOURS = "4h"
                    INTERVAL_1_DAY = "1d"
                    INTERVAL_1_WEEK = "1W"
                    INTERVAL_1_MONTH = "1M
        '''
        #self.interval = interval


    def ma_signal(self, symbol) -> float:
        handler = TA_Handler(
                symbol=symbol,
                exchange="BINANCE",
                screener="crypto",
                interval=Interval.INTERVAL_1_MINUTE
        )

        #print(handler.get_analysis().moving_averages)
        fast = handler.get_analysis().moving_averages["COMPUTE"]["EMA20"]
        slow = handler.get_analysis().moving_averages["COMPUTE"]["EMA50"]
        return fast, slow

    def oscilators(self, symbol):
        handler = TA_Handler(
            symbol=symbol,
            exchange="BINANCE",
            screener="crypto",
            interval=Interval.INTERVAL_1_MINUTE
        )
        rsi = handler.get_analysis().oscillators["COMPUTE"]["RSI"]
        macd = handler.get_analysis().oscillators["COMPUTE"]["MACD"]
        momentum = handler.get_analysis().oscillators["COMPUTE"]["Mom"]

        return rsi, macd, momentum

create_signals = CreateSignals()

def analyze_coin(symbol):
    signalss = [0, 0, 0]

    fast, slow = create_signals.ma_signal(symbol)
    rsi, macd, momentum = create_signals.oscilators(symbol)

    signals = {"FAST_MA": fast, "SLOW_MA": slow,
               "RSI": rsi, "MACD": macd, "MOMENTUM": momentum}

    for name, signal in signals.items():
        if signal == "BUY" or signal == "STRONG_BUY":
            signalss[0] += 1
        elif signal == "SELL" or signal == "STRONG_SELL":
            signalss[1] += 1
        elif signal == "NEUTRAL":
            signalss[2] += 1

    if max(signalss) > 2:
        recomandation = None

        if signalss.index(max(signalss)) == 0:
            recomandation = "Buy"
        elif signalss.index(max(signalss)) == 1:
            recomandation = "Sell"
        elif signalss.index(max(signalss)) == 2:
            recomandation = "Neutral"

        if recomandation and recomandation != prev_signals[symbol][0] and recomandation != prev_signals[symbol][1]:
            print(f"{datetime.datetime.now()} -- {symbol} - Recomandation:[{recomandation}] - Buy:{signalss[0]}, Sell:{signalss[1]}, Neutral:{signalss[2]}")
            return recomandation
            

        prev_signals[symbol][1] = prev_signals[symbol][0]
        prev_signals[symbol][0] = recomandation


# coins sözlüğüne göre prev_signals sözlüğünü oluşturun
coins = {
    "BTCUSDT": "BTCUSDT",
    "ETHUSDT": "ETHUSDT",
    "BLZUSDT": "BLZUSDT",
    "XRPUSDT": "XRPUSDT",
    "1000SHIBUSDT": "1000SHIBUSDT.P",
    "SOLUSDT": "SOLUSDT",
    "BTCBUSD": "BTCBUSD",
    "RUNEUSDT": "RUNEUSDT",
    "BCHUSDT": "BCHUSDT",
    "LTCUSDT": "LTCUSDT",
    "DOGEUSDT": "DOGEUSDT",
    "HBARUSDT": "HBARUSDT",
    "LPTUSDT": "LPTUSDT",
    "LEVERUSDT": "LEVERUSDT",
    "1000PEPEUSDT": "1000PEPEUSDT.P"
}

prev_signals = {symbol: [None, None] for symbol in coins.values()}

while True:
    for coin_symbol in coins.values():
        analyze_coin(coin_symbol)