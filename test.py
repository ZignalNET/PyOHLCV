
import time
from os import environ

import plotly.graph_objects as go

import pyohlcv
from pyohlcv import Luno
from pyohlcv import Binance
from pyohlcv import CoinbasePro
from pyohlcv import Kucoin
from pyohlcv import Kraken
from pyohlcv import Digifinex
from pyohlcv import Idex


print( pyohlcv.exchanges )


luno = Luno(api_key=environ['API_KEY_LUNO'],api_secret=environ['API_SECRET_LUNO'])
since = int(time.time()*1000)-24*60*59*1000
df = luno.fetchOhlcv(symbol='XBTZAR',timeframe='15m',since=since)
if not df.empty: 
	print( df.tail(5) )
	sma10 = df.ta.sma(length=10)
	print(sma10.tail(5))



df = Binance(api_key='',api_secret='').fetchOhlcv(symbol='XRPBTC',timeframe='1m',limit=5000, start_time="2022-01-14 00:00:00", end_time="2022-01-15 23:59:59")
#df = Binance(api_key='',api_secret='').fetchOhlcv(symbol='XRPBTC',timeframe='1m',limit=200)
if not df.empty: 
	print( df.head() )
	print( df.tail(5) )
	sma10 = df.ta.sma(length=10)
	print(sma10.tail(5))




df = CoinbasePro(api_key='',api_secret='').fetchOhlcv(symbol='BTC-USD',timeframe='1d', start_time="2021-01-01 00:00:00", end_time="2021-01-04 10:00:00")
if not df.empty: 
	print( df.head() )
	print( df.tail(5) )



kucoin = Kucoin(api_key='',api_secret='')
df = kucoin.fetchOhlcv(symbol='BTC-USDT',timeframe='1min', start_time="2021-01-01 03:59:59+02:00", end_time="2021-01-02 16:59:59+02:00")
if not df.empty: print( df )



kraken = Kraken(api_key='',api_secret='')
df = kraken.fetchOhlcv(symbol='XBTUSD',timeframe='30m', since="2022-07-10 03:59:59")
if not df.empty: print( df )



digifinex = Digifinex(api_key='',api_secret='')
df = digifinex.fetchOhlcv(symbol='btc_usdt',timeframe='1D', start_time="2021-02-01T03:59:59+02:00", end_time="2022-02-02T16:59:59+02:00")
if not df.empty: print( df )


idex = Idex(api_key='',api_secret='')
df = idex.fetchOhlcv(symbol='ETH-USDC',timeframe='1m', start_time="2022-02-02T14:15:00+02:00", end_time="2022-06-02T05:59:59+02:00")
if not df.empty: 
	print( df )

fig = go.Figure(data=[go.Candlestick(x=df['timestamp'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])

fig.show()





