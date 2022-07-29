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



