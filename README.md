# PyOHLCV
A Python package that fetches historical OHLCV data from supported exchanges into Panda dataframe using python requests and pandas.

## Dependencies
```sh
Requests
Pandas
Pandas_ta
```

## Usage

```sh
from pyohlcv import Luno
luno = Luno(api_key=environ['API_KEY_LUNO'],api_secret=environ['API_SECRET_LUNO'])
since = int(time.time()*1000)-24*60*59*1000
df = luno.fetchOhlcv(symbol='XBTZAR',timeframe='15m',since=since)
if not df.empty: 
	print( df.tail(5) )
	sma10 = df.ta.sma(length=10)
	print(sma10.tail(5))
	
	timestamp       open       high        low      close    volume
89 2022-07-29 07:00:00  400751.00  400782.00  399264.00  399499.00  9.950004
90 2022-07-29 07:15:00  399907.00  400271.00  397224.00  398520.00  6.288367
91 2022-07-29 07:30:00  398906.00  400700.00  397851.00  399898.00  5.567731
92 2022-07-29 07:45:00  399866.00  400900.00  399431.00  400546.00  7.194648
93 2022-07-29 08:00:00  400078.00  400898.00  398462.00  400250.00   3.88822

<p>
<img src="https://user-images.githubusercontent.com/100917638/181716949-3f48ef53-923e-4d9d-9ec6-9358fc8bed0f.png">
</p>

```

```sh
from pyohlcv import Idex
idex = Idex(api_key='',api_secret='')
df = idex.fetchOhlcv(symbol='ETH-USDC',timeframe='1m', start_time="2022-02-02T14:15:00+02:00", end_time="2022-06-02T05:59:59+02:00")
if not df.empty: 
	print( df )
  
  
		timestamp           open           high            low          close      volume  sequence
0     2022-02-02 12:15:00  2785.93000000  2785.93000000  2785.51000000  2785.51000000  0.18000000     67671
1     2022-02-02 12:17:00  2785.08000000  2785.08000000  2785.08000000  2785.08000000  0.11000000     67673
2     2022-02-02 12:19:00  2785.08000000  2785.08000000  2784.74000000  2784.74000000  0.18000000     67675
3     2022-02-02 12:20:00  2783.99000000  2783.99000000  2783.67000000  2783.67000000  0.13000000     67677
4     2022-02-02 12:21:00  2782.95000000  2782.95000000  2782.95000000  2782.95000000  0.21000000     67678
...                   ...            ...            ...            ...            ...         ...       ...
37854 2022-06-02 03:07:00  1825.39000000  1825.39000000  1825.39000000  1825.39000000  0.17000000    284605
37855 2022-06-02 03:36:00  1825.68000000  1825.68000000  1825.68000000  1825.68000000  0.08000000    284606
37856 2022-06-02 03:38:00  1825.13000000  1825.13000000  1824.49000000  1824.49000000  0.20000000    284608
37857 2022-06-02 03:48:00  1823.57000000  1823.57000000  1823.57000000  1823.57000000  0.18000000    284609
37858 2022-06-02 03:53:00  1822.73000000  1822.73000000  1822.16000000  1822.16000000  0.17000000    284612


```

![newplot](https://user-images.githubusercontent.com/100917638/181715844-40490e2e-ee52-4175-bbd5-23fb985834d9.png)


## Supported Exchanges
```sh
import pyohlcv

print( pyohlcv.exchanges )
['Binance', 'Coinbase Pro', 'Luno', 'Kucoin', 'Kraken', 'Digifinex', 'Idex']

```



