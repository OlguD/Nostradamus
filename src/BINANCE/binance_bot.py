from binance.client import Client
from config import API_KEY, API_SECRET  # API anahtarlarınızı buradan alın


# Binance API istemcisini oluşturun
client = Client(API_KEY, API_SECRET)

# Örnek olarak bakiye bilgisini alalım
account_info = client.get_account()
balances = account_info['balances']

# Hesap bakiyesini gösterelim
for balance in balances:
    asset = balance['asset']
    free = balance['free']
    locked = balance['locked']
    print(f"{asset}: Free: {free}, Locked: {locked}")
