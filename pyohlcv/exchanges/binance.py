"""
    Filename    :   binance.py
    Part of     :   pyOHLCV
    By          :   Emmanuel Adigun (emmanuel@zignal.net)
    Date        :   01 July 2022
"""
import pytz
from datetime import datetime, timedelta
from time import sleep
from pandas import DataFrame, to_datetime
from ..base import Base
from ..error import Error

class Binance(Base):

    def __init__(self,**kwargs):
        kwargs.update({'base_url':'https://api.binance.com'})
        super().__init__(**kwargs)
        
    def fetchOhlcv(self,symbol:    str  = 'XRP/BTC', 
                        timeframe: str = '1m',
                        since: str = '',
                        limit:     int = 100,
                        start_time: str = None,
                        end_time: str = None
                  ) -> DataFrame:
        """
            GET /api/v3/klines, returns
                dataframe: DataFrame or empty dataframe, unix timestamp is converted to python datetime object
        """
        # convert interval to econds
        interval = self.parseTimeframe(timeframe) * 1000

        #Max limit; 1000 if start time is not set
        maxrows = min(500,limit) if start_time != None else limit

        #Build request args
        params = dict(symbol=symbol, interval=timeframe,limit=maxrows)
        if start_time != None: params.update({'startTime': self.to_milliseconds(start_time)-interval })
        if end_time   != None: params.update({'endTime': self.to_milliseconds(end_time) })
        args = dict(timeout=self.timeout, params=params, headers=self.generateHeader())

        #Binance KLine endpoint
        url = self.buildURL('/api/v3/klines',{})
        
        # Create dataframe
        df = DataFrame() 
        rows = []
        irow = 0
        while True:
            response = self.perform_request('GET',url,**args)
            if not 'error' in response:
                rrows = len( response['data'] )
                row = []
                for line in response['data']: 
                    row.append([line[0], float(line[1]), float(line[2]), float(line[3]), float(line[4]), float(line[5])])
                #Append to array
                rows += row

                #Reset start datetime
                if start_time != None:
                    lastdate = int(row[len(row) - 1][0])
                    start = (lastdate + interval)/1000
                    start = self.to_milliseconds( datetime.utcfromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S.%f') )
                    args["params"]["startTime"] = start
                else: break

                #Do we have fewer rows? possibly signalling end of iteration
                if rrows < maxrows: break

                irow += 1
                #Be a nice Binance citizen
                if irow % 3 == 0: sleep(1)

            else: 
                print( response['error_text'])
                break

        df = DataFrame(rows, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df['timestamp'] = to_datetime(df['timestamp'], unit='ms')

        return df

    
















        