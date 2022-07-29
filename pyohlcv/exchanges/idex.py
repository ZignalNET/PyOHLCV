"""
    Filename    :   idex.py
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

class Idex(Base):

    def __init__(self,**kwargs):
        kwargs.update({'base_url':'https://api-matic.idex.io'})
        super().__init__(**kwargs)
        
    #https://api-docs-v3.idex.io/#get-candles
    #candlestick patterns: 1m,5m,15m,30m,1h,6h,1d
    def fetchOhlcv(self,symbol:    str  = 'ETH-USDC', 
                        timeframe: str = '1m',
                        since: str = '',
                        limit:     int = 0,
                        start_time: str = None,
                        end_time: str = None
                  ) -> DataFrame:
        """
            GET /v1/candles, returns
                dataframe: DataFrame or empty dataframe, unix timestamp is converted to python datetime object
        """

        #Max limit; 1000 idex max
        maxrows = 1000
        
        #Build request args
        params = dict(market=symbol, interval=timeframe, limit=maxrows)
        args = dict(timeout=self.timeout, params=params, headers=self.generateHeader())



        from_time = to_time = None
        if start_time != None:
            from_time = int(datetime.fromisoformat(start_time).timestamp()*1000)
            args["params"]["start"] = from_time

        if end_time != None:
            to_time   = int(datetime.fromisoformat(end_time).timestamp()*1000)
            args["params"]["end"]   = to_time

        #KLine endpoint
        url = self.buildURL('/v1/candles'.format(),{})
        
        # Create dataframe
        df = DataFrame() 
        rows = []
        irow = 0

        if from_time != None:
            args["params"]["start"] = from_time

        while True:
            response = self.perform_request('GET',url,**args)
            if not 'error' in response and 'data' in response:
                if 'data' in response and isinstance(response['data'], list):
                    lines = response['data']
                    rrows = len( lines )
                    if rrows:
                        #Append to array
                        rows += lines

                        #print(datetime.utcfromtimestamp(from_time/1000).isoformat(), datetime.utcfromtimestamp(to_time/1000).isoformat(), rrows)

                        #Do we have fewer rows? possibly signalling end of iteration
                        if rrows < maxrows: break

                        if from_time != None and end_time != None:
                            last = lines[len(lines)-1]
                            from_time = last["start"]
                            args["params"]["start"] = from_time
                            args["params"]["end"]   = to_time

                            irow += 1
                            #Be nice to the API; or risk BAN!
                            if irow % 3 == 0: sleep(1)

                        else:
                            break

                    else:
                        break

                else:
                    print( response['data'] )
                    break
            
            else: 
                print( response['error_text'] )
                break


        df = DataFrame(rows) #, columns=["timestamp", "open", "high","close", "low", "volume"])
        df['start'] = to_datetime(df['start'], unit='ms')
        df = df.rename(columns={'start': 'timestamp'})

        return df

    
















        