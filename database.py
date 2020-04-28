import sqlite3
from stockscore import Stock

conn = sqlite3.connect(':memory:')

c = conn.cursor()

c.execute("""CREATE TABLE stocks (
            ticker text,
            price integer,
            sentiment integer
            )""")

values = Stock.getScorePrice(['AAPL','FB'])

for v in values:
    tick = v['ticker']
    price = v['price']
    sent_score = v['sentiment']
    c.execute("INSERT INTO stocks VALUES (:ticker, :price, :sentiment)", {'ticker': tick, 'price': price, 'sentiment': sent_score})

conn.commit()

c.execute("SELECT * FROM stocks")

print(c.fetchall())

conn.close()