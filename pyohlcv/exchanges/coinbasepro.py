"""
    Filename    :   coinbasepro.py
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

class CoinbasePro(Base):

    def __init__(self,**kwargs):
        kwargs.update({'base_url':'https://api.pro.coinbase.com'})
        super().__init__(**kwargs)
        
    def fetchOhlcv(self,symbol:    str  = 'BTC-USD', 
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
        #60|1m, 300|5m, 900|15m, 3600, 21600, 86400
        interval  = self.parseTimeframe(timeframe)

        delta     = timedelta(seconds = interval)
        timeStart = None
        timeEnd   = None

        #Max limit; 300 coinbase max
        maxrows = 300

        #Build request args
        params = dict(granularity=str(interval))
        args = dict(timeout=self.timeout, params=params, headers=self.generateHeader())

        to_time = datetime.now()
        if end_time != None: to_time = datetime.fromisoformat(end_time)

        if start_time != None:
            timeStart = datetime.fromisoformat(start_time)
            timeEnd   = timeStart + (maxrows*delta)
            if timeEnd > to_time: timeEnd = to_time

        #KLine endpoint
        url = self.buildURL('/products/{}/candles'.format(symbol),{})
        
        # Create dataframe
        df = DataFrame() 
        rows = []
        irow = 0

        while True:
            if timeStart != None and timeEnd != None:
                args["params"]["start"] = timeStart.isoformat()
                args["params"]["end"]   = timeEnd.isoformat()

            response = self.perform_request('GET',url,**args)
            if not 'error' in response:
                rrows = len( response['data'] )
                row = []
                for line in response['data']: 
                    row.append([line[0], float(line[1]), float(line[2]), float(line[3]), float(line[4]), float(line[5])])

                #Append to array
                rows += row

                #Do we have fewer rows? possibly signalling end of iteration
                if rrows < maxrows: break

                #Do we specify start dates? 
                if start_time == None: break

                #Calc next start and end times for the next cycle
                timeStart = timeEnd
                timeEnd   = timeEnd + (maxrows*delta)
                if timeEnd > to_time: timeEnd = to_time

                if timeStart > to_time: break

                irow += 1
                #Be nice to the API; or risk HTTP code 429
                if irow % 3 == 0: sleep(1)

            else: 
                print( response['error_text'])
                break

        df = DataFrame(rows, columns=['time','low','high','open','close','volume'])
        df['time'] = to_datetime(df['time'], unit='s')

        df = df.set_index('time') 
        df = df.sort_index(ascending=True)
        return df

    
















        