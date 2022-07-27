"""
    Filename    :   kucoin.py
    Part of     :   pyOHLCV
    By          :   Emmanuel Adigun (emmanuel@zignal.net)
    Date        :   03 July 2022
"""
import pytz
from operator import itemgetter
from datetime import datetime, timedelta
from time import sleep
from pandas import DataFrame, to_datetime
from ..base import Base
from ..error import Error

class Kucoin(Base):

    def __init__(self,**kwargs):
        kwargs.update({'base_url':'https://api.kucoin.com'})
        super().__init__(**kwargs)
        
    #https://docs.kucoin.com/#get-klines
    #candlestick patterns: 1min, 3min, 5min, 15min, 30min, 1hour, 2hour, 4hour, 6hour, 8hour, 12hour, 1day, 1week
    def fetchOhlcv(self,symbol:    str  = 'BTC-USDT', 
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
        
        #Max limit; 1500 by kucoin 
        maxrows = min(1500,limit)

        #Build request args
        params = dict(symbol=symbol, type=timeframe)
        args = dict(timeout=self.timeout, params=params, headers=self.generateHeader())


        from_time = int(datetime.fromisoformat(start_time).timestamp())
        to_time   = int(datetime.now().timestamp()) if end_time == None else int(datetime.fromisoformat(end_time).timestamp())

        if start_time != None: params.update({'startAt': from_time })
        if end_time   != None: params.update({'endAt':   to_time})

        #KLine endpoint
        url = self.buildURL('/api/v1/market/candles'.format(),{})
        
        # Create dataframe
        df = DataFrame() 
        rows = []
        irow = 0
        while True:
            if start_time != None: params.update({'startAt': from_time })
            response = self.perform_request('GET',url,**args)
            if not 'error' in response:
                if 'data' in response['data']:
                    lines = response['data']['data']
                    rrows = len( lines )
                    row = []
                    for line in lines: 
                        row.append([int(line[0]), float(line[1]), float(line[2]), float(line[3]), float(line[4]), float(line[5]), float(line[6])])
                  
                    #Sort by timestamp column
                    row = sorted(row, key=itemgetter(0))

                    #Append to array
                    rows += row

                    #Reset start datetime
                    if start_time != None and len(row) > 0:
                        from_time = int(row[len(row) - 1][0])
                        sleep(1)
                    else: break

                    #Do we have fewer rows? possibly signalling end of iteration
                    if rrows < maxrows: break
                    
                else:
                    print( response['data'] )
                    break
            else: 
                print( response['error_text'])
                break

        df = DataFrame(rows, columns=["timestamp", "open", "close","high", "low", "volume","turnover"])
        df['timestamp'] = to_datetime(df['timestamp'], unit='s')

        return df

    
















        