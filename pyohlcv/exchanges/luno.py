"""
    Filename    :   luno.py - LUNO
    Part of     :   pyOHLCV
    By          :   Emmanuel Adigun (emmanuel@zignal.net)
    Date        :   01 July 2022
"""
from pandas import DataFrame
from ..base import Base
from ..error import Error

class Luno(Base):
    LUNO_KLINE_1M           = 60 
    LUNO_KLINE_5M           = 300
    LUNO_KLINE_15M          = 900
    LUNO_KLINE_30M          = 1800
    LUNO_KLINE_1H           = 3600
    LUNO_KLINE_3H           = 10800
    LUNO_KLINE_4H           = 14400 
    LUNO_KLINE_8H           = 28800
    LUNO_KLINE_24H          = 86400
    LUNO_KLINE_3D           = 259200 
    LUNO_KLINE_7D           = 604800

    def __init__(self,**kwargs):
        kwargs.update({'base_url':'https://api.luno.com'})
        super().__init__(**kwargs)
        self.klines = {}
        self.init_klines()

    def init_klines(self):
        self.klines['1M']     = 60
        self.klines['5M']     = 300
        self.klines['15M']     = 900
        self.klines['30M']     = 1800
        self.klines['1H']     = 3600
        self.klines['3H']     = 10800
        self.klines['4H']     = 14400
        self.klines['8H']     = 28800
        self.klines['24H']     = 86400
        self.klines['3D']     = 259200
        self.klines['7D']     = 604800

    def fetchOhlcv(self,symbol:    str  = 'XBTZAR', 
                        timeframe: str = '1m',
                        since:     int = 0,   # UNIX timestamp 
                        limit:     int = 100
                  ) -> DataFrame:
        """
            GET /api/exchange/1/candles
        """
        period = Luno.LUNO_KLINE_1M
        if timeframe.upper() in self.klines: period = self.klines[timeframe.upper()]
        params = dict(pair=symbol, duration=period, since=since)
        url = self.buildURL('/api/exchange/1/candles',params)
        args = dict(timeout=self.timeout, params=params, headers=self.generateHeader(), auth=(self.api_key, self.api_secret))
        response = self.perform_request('GET',url,**args)
        if not 'error' in response:
            lines = response['data']
            if 'candles' in lines:
                print( len(lines['candles']) )
                print( lines['candles'][0] )
        else: print( response['error_text'])
















        