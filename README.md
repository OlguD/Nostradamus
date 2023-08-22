# TradeBot
Gives Buy/Sell signals in real time, also it has telegram bot.

### Usage
1. For activating virtual environment macOS: `source venv/bin/activate`
2. `pip install -r requirements`
3. Then you are inside 
4. For getting all the coin signals, you need to simply run `main.py` file
5. But if you want to get only one coin signal you need to run `TELEGRAM_BOT/one_coin.py`
6. If you want to run the telegram bot, you need to comment out the last 3 columns in one_coin.py
7. For deactivating virtual environment: `deactivate`

Example of output: 
2023-08-23 00:10:47.098476 -- BTCUSDT - Recomandation:[Sell] - Buy:1, Sell:3, Neutral:1

### Development Process
* Program must be tested in `BACTEST/backtest.py`, should be tested by creating a simulation environment according to the signals given by the program, for example, a user balance of 1000 TL, and the profit / loss situation should be tested during the time the user runs the program 
* Then binance bot must be developed
* Program should be run in the VPS server for running 24/7
* Users can be start the program via Telegram.

