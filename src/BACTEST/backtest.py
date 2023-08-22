import sqlite3
from src.one_coin import analyze_coin

conn = sqlite3.connect("user.db")

## İşlemleri burada gerçekleştir
while True:
    result = analyze_coin("BTCUSDT")
    if result is not None:
        print(result)

# Bağlantıyı kapat
conn.close()