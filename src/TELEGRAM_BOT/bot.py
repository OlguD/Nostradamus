import telebot
from config import TOKEN
from BotClass.bot import *
import time

bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands=['start'])
def send_welcome(message):
	name = message.from_user.first_name
	capitalized_msg = name.capitalize()

	bot.reply_to(message, "Hi " + capitalized_msg) 


@bot.message_handler(['coins'])
def info_message(message):
	text = """
	Coins: 
	 "BTCUSDT"
    "ETHUSDT"
    "BLZUSDT"
    "XRPUSDT"
    "1000SHIBUSDT"
    "SOLUSDT"
    "BTCBUSD"
    "RUNEUSDT"
    "BCHUSDT"
    "LTCUSDT"
    "DOGEUSDT"
    "HBARUSDT"
    "LPTUSDT"
    "LEVERUSDT"
    "1000PEPEUSDT"
	"""
	bot.reply_to(message, text)

@bot.message_handler(['help'])
def help_message(message):
	text = """
	This bot generates signals for the coins you see belove

	Commands:
	 - /start
	 - /help
	 - /coins

	 !!! for getting the coin data just write how you see with coins command
	"""
	bot.reply_to(message, text)



@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text
    chat_id = message.chat.id
    onecoin = OneCoin(user_input)

    if user_input == "/stop":
        bot.send_message(chat_id, "Analiz sonlandırıldı.")
        return

    if user_input in coins:
        coin = onecoin
        while True:
            result = onecoin.analyze()
            if result is not None:
                bot.send_message(chat_id, result)
            #time.sleep(60)  # 60 saniye (1 dakika) bekleme süresi
    else:
        bot.send_message(chat_id, "Geçersiz coin adı. Lütfen geçerli bir coin adı girin.")


bot.infinity_polling()
