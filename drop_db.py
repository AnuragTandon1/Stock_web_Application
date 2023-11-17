import sqlite3
connection =sqlite3.connect('app.db')
cursor = connection.cursor()
cursor.execute("""
               DROP table strategy
               """)
cursor.execute("""
               DROP table stock_strategy
               """)

connection.commit()