import sqlite3 , config
from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")
@app.get("/")
def index(request: Request):
    print(dir(request))
    connection =sqlite3.connect('app.db')
    connection.row_factory = sqlite3. Row
    cursor = connection.cursor()
    cursor.execute("""
               SELECT symbol,name from stock
               """)
    rows=cursor.fetchall()
    return templates.TemplateResponse("index.html", {"request": request, "stocks": rows})
@app.get("/stock/{symbol}")
def stock_detail(request: Request,symbol):
    connection =sqlite3.connect('app.db')
    connection.row_factory = sqlite3. Row
    cursor = connection.cursor()
    cursor.execute("""
               SELECT id,symbol,name FROM stock WHERE symbol = ?
               """,(symbol,))
    row=cursor.fetchone()
    cursor.execute ("""
                    SELECT * FROM stock_price WHERE stock_id = ?
                    """, (row['id'],))
    prices = cursor. fetchall ()
    return templates.TemplateResponse("stock_detail.html", {"request": request, "stock": row,"prices": prices})
   