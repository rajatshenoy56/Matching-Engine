import _thread
import random
import time
from bs4 import BeautifulSoup
import requests
import requests_html

stocks = {
    "BHARTIARTL.NS": 100, 
    "TCS.NS": 500, 
    "HDFCBANK.NS": 250, 
    "SBIN.NS": 213, 
    "INFY.NS": 345
}

def getPricesOnline():
    for key in stocks:
        url = 'https://in.finance.yahoo.com/quote/'+key
        session = requests_html.HTMLSession()
        r = session.get(url)
        content = BeautifulSoup(r.content, 'lxml')
        price = str(content).split('data-reactid="32"')[4].split('</span>')[0].replace('>','')
        price = float(price.replace(',',''))
        stocks[key] = price
    

def computePrices():
    count = 0
    getPricesOnline()
    while True:
        if count == 5:
            getPricesOnline()
            count = 0
        else:
            for key in stocks:
                percent = random.uniform(-1,1)
                stocks[key] += stocks[key]*percent/100
            count+=1
        time.sleep(2)
    
_thread.start_new_thread(computePrices, ())