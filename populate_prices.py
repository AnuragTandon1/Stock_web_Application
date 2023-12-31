import sqlite3 ,config
import alpaca_trade_api  as tradeapi
connection =sqlite3.connect('app.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
cursor.execute("""
               select id ,symbol,name from stock
               
               """)
rows = cursor.fetchall()
symbols =[]
stock_dict = {}
for row in rows:
    symbol = row['symbol']
    symbols.append(symbol)
    stock_dict[symbol] = row['id']

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url='https://api.alpaca.markets')
chunk_size = 200
for i in range(0, len (symbols), chunk_size):
    symbol_chunk = symbols[i:i+ chunk_size]
    
    barsets = api.barset(symbol_chunk,'day')
    for symbol in barsets:
        print(f"processing symbol {symbol}")
        for bar in barsets[symbol]:
            stock_id = stock_dict[symbol]
            cursor.execute("""
               insert into stock_price(stock_id,date,open,high,low,close,volume) VALUES(?,?,?,?,?,?,?)
               
               """,(stock_id, bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v))
            
connection.commit()






