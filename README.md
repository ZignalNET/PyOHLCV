# PyOHLCV
A Python package that fetches historical OHLCV data from supported exchanges into Panda dataframe

## Usage
```sh
e = EtherChainPy(apikey=environ['API_KEY_ETHERSCAN'], conversion_api_key=<from min-cryptocompare>)
print(e.geth.getGasPrice(to="WEI"))
11914121454

print(e.geth.getGasPrice(to="GWEI"))
11.914121454

