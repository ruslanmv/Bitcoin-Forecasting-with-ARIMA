from django.shortcuts import render
from .models import Sale
from .utils import get_plot
from pmdarima import auto_arima
import time
# Create your views here.

def main_view(request):
   # qs = Sale.objects.all()
   # x = [x.item for x in qs]
   # y = [y.price for y in qs]
   # x =['uno', 'due','tree']
   # y =[10,20,30]
    import yfinance as yf
    import pandas as pd
   # gold = yf.Ticker("GC=F")
   # get historical market data
   # hist = gold.history(period="5d")
   # hist.to_csv("Gold-now.csv")

   # bitcoin = yf.Ticker("BTC-USD")
   # get historical market data
   # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
   # hist = bitcoin.history(period="3mo")
   # hist.to_csv("Bitcoin-now.csv")
   # df = pd.read_csv("Bitcoin-now.csv")
    #time.sleep(1)  # to avoid multiple calls
    df = yf.download("BTC-USD", period="1y")
    #df.to_csv("Bitcoin-last.csv")
    #df = pd.read_csv("Bitcoin-last.csv")
    #df = pd.read_csv("Gold.csv")
    #df = pd.read_csv("BTC-USD.csv")
#    x=range(0, len(df['Date']))
#    y=df['Open'].tolist()
    df=df.dropna()
    best_order = auto_arima(df['Close'], trace = True)
    order=best_order.order
    columns = ['Close']
    df=pd.DataFrame(df, columns=columns)
    df=df.reset_index(drop=True)
    train, test = df[0:int(len(df)*0.85)], df[int(len(df)*0.85):]
    from statsmodels.tsa.arima_model import ARIMA 
    model = ARIMA (train, order=order)
    model = model.fit()
    #start=len(train)               ##Example= y1,y2,y3 > y3-y2,y2-y1 (Total elements is 3 but after using Arima its 2 > data- 1 
    #end=len(train)+len(test)-1
    start=1
    end=len(df)

    pred=model.predict(start=start,end=end,typ='levels').rename('ARIMA Predictions')
   
    y=pred
    x=range(0, len(df))
    z=test['Close']
    w=train['Close']
    chart = get_plot(x,y,z,w)
    return render(request, 'sales/main.html',{'chart':chart})
