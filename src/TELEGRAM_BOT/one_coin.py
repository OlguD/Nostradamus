import math
from tradingview_ta import TA_Handler, Interval
import datetime


def ma_signal(symbol):
    handler = TA_Handler(
            symbol=symbol,
            exchange="BINANCE",
            screener="crypto",
            interval=Interval.INTERVAL_5_MINUTES
    )

    #print(handler.get_analysis().moving_averages)
    fast = handler.get_analysis().moving_averages["COMPUTE"]["EMA20"]
    slow = handler.get_analysis().moving_averages["COMPUTE"]["EMA50"]
    return fast, slow


def oscilators(symbol):
    handler = TA_Handler(
        symbol=symbol,
        exchange="BINANCE",
        screener="crypto",
        interval=Interval.INTERVAL_5_MINUTES
    )
    rsi = handler.get_analysis().oscillators["COMPUTE"]["RSI"]
    macd = handler.get_analysis().oscillators["COMPUTE"]["MACD"]
    momentum = handler.get_analysis().oscillators["COMPUTE"]["Mom"]

    return rsi, macd, momentum

    
#def calculate_rsih(symbol, length):
#    cu = 0.0
#    cd = 0.0
#    PIx2 = 2 * math.pi

#    handler = TA_Handler(
#        symbol=symbol,
#        exchange="BINANCE",
#        screener="crypto",
#        interval=Interval.INTERVAL_1_MINUTE
#    )
#    change_values = handler.get_analysis().indicators["change"]  # Bu kısmı kütüphaneye göre güncellemelisiniz

#    for count in range(1, length):
#        change = change_values[count]  # Doğru şekilde indikatör değerine erişim sağlayın
#        absChange = abs(change)
#        cosPart = math.cos(PIx2 * count / (length + 1))

#        if change < 0:
#            cu += (1 - cosPart) * absChange
#        elif change > 0:
#            cd += (1 - cosPart) * absChange

#    result = (cu - cd) / (cu + cd)
#    return result



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
prev_signals = [None, None]

def analyze_coin(symbol):
    coin = coins[symbol]
    signalss = [0, 0, 0]

    fast, slow = ma_signal(coin)
    rsi, macd, momentum = oscilators(coin)

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

        if recomandation and recomandation != prev_signals[0] and recomandation != prev_signals[1]:
            current_output = f"{datetime.datetime.now()} -- {symbol} - Recomandation:[{recomandation}] - Buy:{signalss[0]}, Sell:{signalss[1]}, Neutral:{signalss[2]}"
            return recomandation

            prev_signals[1] = prev_signals[0]
            prev_signals[0] = recomandation


# Telegram botunu çalıştırmadan önce aşağıdaki satırları yorum satırı yap !!! s
#while True:
#    result = analyze_coin("BTCUSDT")
#    if result is not None:
#        print(result)
