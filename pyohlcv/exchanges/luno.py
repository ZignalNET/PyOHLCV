"""
    Filename    :   luno.py
    Part of     :   pyOHLCV
    By          :   Emmanuel Adigun (emmanuel@zignal.net)
    Date        :   01 July 2022
"""
from pandas import DataFrame, to_datetime
from ..base import Base
from ..error import Error

class Luno(Base):

    def __init__(self,**kwargs):
        kwargs.update({'base_url':'https://api.luno.com'})
        super().__init__(**kwargs)


    def fetchOhlcv(self,symbol:    str  = 'XBTZAR', 
                        timeframe: str = '1m',
                        since: str = '',
                        limit:     int = 100,
                        start_time: str = None,
                        end_time: str = None
                  ) -> DataFrame:
        """
            GET /api/exchange/1/candles, returns
                dataframe: DataFrame or empty dataframe, unix timestamp is converted to python datetime object
        """
        #parse 1m,3m into required time formats
        period = self.parseTimeframe(timeframe)

        #Build request args
        params = dict(pair=symbol, duration=period, since=since)
        args = dict(timeout=self.timeout, params=params, headers=self.generateHeader(), auth=(self.api_key, self.api_secret))

        #Luno OHLCV endpoint
        url = self.buildURL('/api/exchange/1/candles',params)
        
        response = self.perform_request('GET',url,**args)
        df = DataFrame()  #default return value
        if not 'error' in response:
            lines = response['data']
            if 'candles' in lines:
                df = DataFrame(data=lines['candles'], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                df['timestamp'] = to_datetime(df['timestamp'], unit='ms')
        else: print( response['error_text'])
        return df
















        