import math
from tradingview_ta import TA_Handler, Interval
import datetime


class Calculation:
    def __init__(self, interval=Interval.INTERVAL_5_MINUTES, exchange="BINANCE", screener="crypto"):
        ''' 
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
                
        exchange - BINANCE, BIST
        '''
        self.prev_signals = {}
        self.interval = interval
        self.exchange = exchange
        self.screener = screener

    def ma_signal(self, symbol) -> float:
        handler = TA_Handler(
                symbol=symbol,
                exchange=self.exchange,
                screener=self.screener,
                interval=self.interval
        )

        #print(handler.get_analysis().moving_averages)
        fast = handler.get_analysis().moving_averages["COMPUTE"]["EMA20"]
        slow = handler.get_analysis().moving_averages["COMPUTE"]["EMA50"]
        return fast, slow

    def oscilators(self, symbol):
        handler = TA_Handler(
                symbol=symbol,
                exchange=self.exchange,
                screener=self.screener,
                interval=self.interval
        )
        rsi = handler.get_analysis().oscillators["COMPUTE"]["RSI"]
        macd = handler.get_analysis().oscillators["COMPUTE"]["MACD"]
        momentum = handler.get_analysis().oscillators["COMPUTE"]["Mom"]

        return rsi, macd, momentum

    def analyze_coin(self, symbol):
        
        # if symbol not in self.prev_signals:
        #     self.prev_signals[symbol] = [None, None]  # Her sembol için önceki sinyalleri saklamak için bir liste

        # prev_signals = self.prev_signals[symbol]

        signalss = [0, 0, 0]

        fast, slow = self.ma_signal(symbol)
        rsi, macd, momentum = self.oscilators(symbol)

        signals = {"FAST_MA": fast, "SLOW_MA": slow,
                "RSI": rsi, "MACD": macd, "MOMENTUM": momentum}

        for name, signal in signals.items():
            if signal == "BUY" or signal == "STRONG_BUY":
                signalss[0] += 1
            elif signal == "SELL" or signal == "STRONG_SELL":
                signalss[1] += 1
            elif signal == "NEUTRAL":
                signalss[2] += 1


        # if max(signalss) > 2:
        recomandation = None

        if signalss.index(max(signalss)) == 0:
            recomandation = "Buy"
        elif signalss.index(max(signalss)) == 1:
            recomandation = "Sell"
        elif signalss.index(max(signalss)) == 2:
            recomandation = "Neutral"
        
        # if recomandation and recomandation != prev_signals[0] and recomandation != prev_signals[1]:
        result = f"{datetime.datetime.now()} -- {symbol} - Recomandation:[{recomandation}] - Buy:{signalss[0]}, Sell:{signalss[1]}, Neutral:{signalss[2]}"
        return recomandation, signalss[0], signalss[1], signalss[2]

        # self.prev_signals[1] = self.prev_signals[0]
        # self.prev_signals[0] = recomandation
            

            

# prev_signals = {symbol: [None, None] for symbol in coins.values()}

# while True:
#     for coin_symbol in coins.values():
#         analyze_coin(coin_symbol)

class ForexSignals:
    def __init__(self, symbol):
        self.symbol = symbol
        self.calculation = Calculation(interval=Interval.INTERVAL_1_WEEK, exchange="BIST", screener="turkey")
        self.prev_signals = {self.symbol: [None, None]}

    def analyze(self):
        recomandation, signal1, signal2, signal3 = self.calculation.analyze_coin(self.symbol)
        prev_signals = self.prev_signals[self.symbol]

        if recomandation and recomandation != prev_signals[0] and recomandation != prev_signals[1]:
            self.prev_signals[self.symbol][1] = self.prev_signals[self.symbol][0]
            self.prev_signals[self.symbol][0] = recomandation

            return recomandation, signal1, signal2, signal3

        else:
            self.prev_signals[self.symbol][1] = self.prev_signals[self.symbol][0]
            self.prev_signals[self.symbol][0] = recomandation


#forex = ForexSignals("ALGYO")
#while True:
#    result = forex.analyze()
#    if result is not None:
#        print(result)


class OneCoin:
    def __init__(self, symbol):
        self.symbol = symbol
        self.calculation = Calculation()
        self.prev_signals = {self.symbol: [None, None]}

    def analyze(self):
        recomandation, signal1, signal2, signal3 = self.calculation.analyze_coin(self.symbol)
        prev_signals = self.prev_signals[self.symbol]

        if recomandation and recomandation != prev_signals[0] and recomandation != prev_signals[1]:
            # result = f"{datetime.datetime.now()} -- {self.symbol} - Recomandation:[{recomandation}] - Buy:{signal1}, Sell:{signal2}, Neutral:{signal3}"
            self.prev_signals[self.symbol][1] = self.prev_signals[self.symbol][0]
            self.prev_signals[self.symbol][0] = recomandation
            return recomandation, signal1, signal2, signal3
        else:
            self.prev_signals[self.symbol][1] = self.prev_signals[self.symbol][0]
            self.prev_signals[self.symbol][0] = recomandation
        

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
        self.coins = {
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
        self.calculation = Calculation()
        self.prev_signals = {symbol: [None, None] for symbol in self.coins.values()}

    def analyze(self, symbol):
        recomandation, signal1, signal2, signal3 = self.calculation.analyze_coin(symbol)

        prev_signals = self.prev_signals[symbol]

        if recomandation and recomandation != prev_signals[0] and recomandation != prev_signals[1]:
            #result = f"{datetime.datetime.now()} -- {symbol} - Recomandation:[{recomandation}] - Buy:{signal1}, Sell:{signal2}, Neutral:{signal3}"
            prev_signals[1] = prev_signals[0]
            prev_signals[0] = recomandation
            if recomandation != None and signal1 != None and signal2 != None and signal3 != None:
                return recomandation, signal1, signal2, signal3
        else:
            prev_signals[1] = prev_signals[0]
            prev_signals[0] = recomandation

# multicoin = MultiCoin()
# while True:
#     for symbol in multicoin.coins.values():
#         result = multicoin.analyze(symbol)
#         if result != None:
#             print(result)

# onecoin = OneCoin('BTCUSDT')
# while True:
#     result = onecoin.analyze()
#     if result is not None:  # None kontrolü ekledim
#         print(result)

# calculation = Calculation()
# while True:
#     calculation.analyze_coin('BTCUSDT')
