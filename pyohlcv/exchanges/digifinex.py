"""
    Filename    :   digifinex.py
    Part of     :   pyOHLCV
    By          :   Emmanuel Adigun (emmanuel@zignal.net)
    Date        :   27 July 2022
"""
import pytz
from operator import itemgetter
from datetime import datetime, timedelta
from time import sleep
from pandas import DataFrame, to_datetime
from ..base import Base
from ..error import Error

class Digifinex(Base):

    def __init__(self,**kwargs):
        kwargs.update({'base_url':'https://openapi.digifinex.com'})
        super().__init__(**kwargs)
        
    #https://docs.digifinex.com/en-ww/v3/#get-candles-data
    #candlestick patterns: 1,5,15,30,60,240,720,1D,1W
    def fetchOhlcv(self,symbol:    str  = 'XBTUSD', 
                        timeframe: str = '1min',
                        since: str = '',
                        limit:     int = 100,
                        start_time: str = None,
                        end_time: str = None
                  ) -> DataFrame:
        """
            GET /api/v1/market/candles, returns
                dataframe: DataFrame or empty dataframe, unix timestamp is converted to python datetime object
        """
        
        #Build request args
        params = dict(symbol=symbol, period=timeframe)
        args = dict(timeout=self.timeout, params=params, headers=self.generateHeader())


        from_time = to_time = None
        if start_time != None:
            from_time = int(datetime.fromisoformat(start_time).timestamp()*1000)
            to_time   = int(datetime.now().timestamp()) if end_time == None else int(datetime.fromisoformat(end_time).timestamp()*1000)

        #KLine endpoint
        url = self.buildURL('/v3/kline'.format(),{})
        
        # Create dataframe
        df = DataFrame() 
        rows = []
        irow = 0

        response = self.perform_request('GET',url,**args)
        if not 'error' in response:
            if 'data' in response['data'] and 'code' in response['data']:
                lines = response['data']['data']
                code   = int(response['data']['code'])

                if code == 0: #Success
                    row = []
                    for line in lines: 
                        row.append([int(line[0]), float(line[5]), float(line[3]), float(line[2]), float(line[4]), float(line[1])])
                  
                    #Sort by timestamp column
                    row = sorted(row, key=itemgetter(0))

                    #Append to array
                    rows += row
                

            else:
                print( response['data'] )
        
        else: 
            print( response['error_text'])


        df = DataFrame(rows, columns=["timestamp", "open", "high","close", "low", "volume"])
        df['timestamp'] = to_datetime(df['timestamp'], unit='s')

        return df

    
















        