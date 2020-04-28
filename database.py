import sqlite3
from stockscore import getScore

conn = sqlite3.connect(':memory:')

c = conn.cursor()

c.execute("""CREATE TABLE stocks (
            ticker text,
            score integer
            )""")

values = getScore(['AAPL','FB'])

for v in values:
    tick = v['ticker']
    sent_score = v['sentiment']
    c.execute("INSERT INTO stocks VALUES (:ticker, :score)", {'ticker': tick, 'score': sent_score})

conn.commit()

c.execute("SELECT * FROM stocks")

print(c.fetchall())

conn.close()