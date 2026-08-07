import sqlite3

import matplotlib.pyplot as plt
import yfinance as yf


def get_stock_data(symbol):
    stock=yf.download(symbol,period='1y')
    return stock
    

def calculator(stock):
     value=stock.iloc[0: ,0]
     av=value.mean()
     ma=value.max()
     mi=value.min()
     up=int((value.diff()>0).sum())
     down=int((value.diff()<0).sum())
     print(av,ma,mi,up,down)
     return av,ma,mi,up,down

def visualization(data,symbol):
     plt.plot(data.index,data.iloc[:,0])
     plt.xlabel("date")
     plt.ylabel("price")
     plt.title(symbol+"stock price")
     plt.show()

file=sqlite3.connect('stocks.sqlite')  
cur=file.cursor()

cur.execute(''' CREATE TABLE IF NOT EXISTS Stocks(
    ID INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT UNIQUE,
    Symbol TEXT UNIQUE,
    Average_Price INTEGER,
    High INTEGER,
    Low INTEGER,
    Up INTEGER,
    Down INTEGER)''')  
file.commit()

def save_stocks(Symbol,Average_Price,High,Low,Up,Down):
     cur.execute('''INSERT OR IGNORE INTO Stocks(Symbol,Average_Price,High,Low,Up,Down) VALUES(?,?,?,?,?,?)''',
                 (Symbol,Average_Price,High,Low,Up,Down))
     file.commit()
     print("saved",Symbol,Up,Down)

def scrape_stocks(s):
     cur.execute(''' SELECT Symbol,Average_Price,High,Low,Up,Down FROM Stocks WHERE symbol=?''',
                 (s,))     
     rows=cur.fetchall()
     for row in rows:
          print("symbol", row[0])
          print('average price',row[1])
          print('high',row[2])
          print('low',row[3])
          print('up days',row[4])
          print('down days',row[5])
          print('____________________________________________________________________________________________')

while True:
    print('\n1.search stocks')
    print('2.search saved stocks')
    print('3.quit')

    choice=input('choose:')    

    if choice=='1':
        symbol=input('enter the stocks:')
        stock=get_stock_data(symbol)
        average_price,high,low,up,down=calculator(stock)
        save_stocks(symbol,average_price,high,low,up,down)
        visualization(stock,symbol)
        

    elif choice=='2':
        symbol=input('enter the symbol:')
        scrape_stocks(symbol)

    elif choice=='3':
        break        


    













    
    

   
# %%
