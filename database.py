import sqlite3

conn = sqlite3.connect('stocks.db')

c = conn.cursor()

# c.execute("""CREATE TABLE stocks (
#             ticker text,
#             score integer
#             )""")

# c.execute("INSERT INTO stocks VALUES ('AAPL', 0.66)")

c.execute("SELECT * FROM stocks")

print(c.fetchone())

conn.commit()

conn.close()