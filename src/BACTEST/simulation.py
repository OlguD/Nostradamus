import json
import requests
import datetime
import sys
sys.path.append('../')
from TELEGRAM_BOT.one_coin import analyze_coin

def get_coin_prices():
    url = 'https://api.binance.com/api/v3/ticker/price?symbol=LEVERUSDT'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    prev_price = []
    count = 0

    while True:
        data = requests.get(url, headers=headers)
        #print(req.status_code)
        data = data.json()
        price = data["price"]
        prev_price.append(price)

        count += 1
        result = analyze_coin("LEVERUSDT")
        buy_sell = {}
        if count > 2:
            if prev_price[-2] != price:
                if result != None and price != None:
                    count+=1
                    buy_sell["Price"] = float(price)
                    buy_sell["Result"] = result
                    return buy_sell
                    
                count+=1

        if len(prev_price) > 1000:
            prev_price = prev_price[500:]


def profit_stop_function(buy_price, multiplier) -> float:
    stop = buy_price + (buy_price * multiplier)
    #loss = buy_price - (buy_price * multiplier)
    
    return stop

prev = {}
count = 0
balance = 1000
total_profit = 0  # Toplam kar/zarar

while True:
    result = get_coin_prices()
    #print(result)
    
    if result["Result"] == "Buy":
        if balance > 0:
            stock = balance / result["Price"]
            prev["Stock"] = stock
            prev["LastSignal"] = "Buy"
            prev["Count"] = count
            prev["BuyPrice"] = result["Price"]
            balance = 0
            prev["Balance"] = balance
            count += 1
            print("Buy:", prev)

    if result["Result"] == "Sell" and prev.get("LastSignal") == "Buy":
        if prev['BuyPrice'] < profit_stop_function(prev['BuyPrice'], 0.1):
            if "Stock" in prev:
                earnings = result["Price"] * prev["Stock"]
                balance = earnings
                prev["Balance"] = balance
                prev["LastSignal"] = "Sell"
                prev["SellPrice"] = result["Price"]
                count += 1
                
                # Calculate profit/loss from this trade
                profit_loss = earnings - (prev["BuyPrice"] * prev["Stock"])
                total_profit += profit_loss
                
                print("Sell:", prev)
                print("Profit/Loss from this trade:", profit_loss)
                print("Total Profit/Loss:", total_profit)
        
        # Here you can add additional logic for holding, stop-loss, etc.

