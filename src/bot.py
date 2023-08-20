import telebot

bot = telebot.TeleBot("5831727023:AAGXOrNOGn7I93_feiN5uUf-vxS2xFDavtQ", parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Merhaba Değirmenci !")

@bot.message_handler()
def help_message(message):
	text = """
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

	This bot generates signals for the coins you see above
	"""
	bot.reply_to(message, text)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.infinity_polling()