
import time
from os import environ
from pyohlcv import Luno

luno = Luno(api_key=environ['API_KEY_LUNO'],api_secret=environ['API_SECRET_LUNO'])
since = int(time.time()*1000)-24*60*59*1000
luno.fetchOhlcv(symbol='XBTZAR',timeframe='5M',since=since)

