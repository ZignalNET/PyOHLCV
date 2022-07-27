"""
    Filename    :   kraken.py
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

class Kraken(Base):

    def __init__(self,**kwargs):
        kwargs.update({'base_url':'https://api.kraken.com'})
        super().__init__(**kwargs)
        
    #https://docs.kraken.com/rest/#tag/Market-Data/operation/getOHLCData
    #candlestick patterns: 1 5 15 30 60 240 1440 10080 21600 in mins
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

        interval  = self.parseTimeframe(timeframe)/60
        
        #Max limit; 720 by kraken 
        maxrows = min(720,limit)

        #Build request args
        params = dict(pair=symbol, type=interval)
        args = dict(timeout=self.timeout, params=params, headers=self.generateHeader())


        from_time = None
        if since != '': 
            from_time = int(datetime.fromisoformat(since).timestamp())

        #KLine endpoint
        url = self.buildURL('/0/public/OHLC'.format(),{})
        
        # Create dataframe
        df = DataFrame() 
        rows = []
        irow = 0

        #If you can get the since parameter to work past certain dates; then good luck!
        #https://stackoverflow.com/questions/48508150/kraken-api-ohlc-request-doesnt-honor-the-since-parameter

        if from_time != None: params.update({'since': from_time })
        response = self.perform_request('GET',url,**args)
        if not 'error' in response:
            if 'result' in response['data']:
                result = response['data']['result']

                lines = list(result.values())[0]
                last  = list(result.values())[1]
                
                row = []
                for line in lines: 
                    row.append([int(line[0]), float(line[1]), float(line[2]), float(line[3]), float(line[4]), float(line[6])])
              
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

    
















        