"""
    Filename    :   base.py - Base file for exchanges
    Part of     :   pyOHLCV 1.0.04
    By          :   Emmanuel Adigun (emmanuel@zignal.net)
    Date        :   01 July 2022
"""
import platform
import requests
from datetime import datetime, timedelta
import time
import pytz
from json.decoder import JSONDecodeError
from typing import Dict
from pandas import DataFrame
import pandas_ta as ta

from .error import Error

class Base:
    """
    pyOHLCV Base Module
    """
    VERSION                 = "1.0.04"
    DEFAULT_SESSION_TIMEOUT = 10

    def __init__(self,**kwargs):
        self.api_key    = kwargs["api_key"]
        self.api_secret = kwargs["api_secret"]
        self.base_url   = kwargs["base_url"]

        self.session    = requests.Session()
        self.timeout    = Base.DEFAULT_SESSION_TIMEOUT
        if 'timeout' in kwargs: self.timeout = kwargs["timeout"]

    def generateHeader(self) -> Dict:
        """
        Returns default header with user agent; sub classes can add more
        """
        PYTHON_VERSION  = platform.python_version()
        SYSTEM          = platform.system()
        MACHINE         = platform.machine()
        return {'User-Agent': "PyOHLCV/{} python/{} {} {} {}".format(Base.VERSION, PYTHON_VERSION, SYSTEM, MACHINE, time.time())}

    def parseTimeframe(self, timeframe: str = '1m'):
        """
        Parse timeframe
        """
        unit     = int(timeframe[0:-1])
        period   = timeframe[-1]
        multiplier = 60 #default 1m
        if   period == 'h': multiplier =  multiplier ** 2
        elif period == 'd': multiplier = (multiplier ** 2) * 24
        elif period == 'w': multiplier = (multiplier ** 2) * 24 * 7
        elif period == 'M': multiplier = (multiplier ** 2) * 24 * 30
        elif period == 'y': multiplier = (multiplier ** 2) * 24 * 365  # Needs to account for leap year if need be
        
        return (multiplier*unit)


    def buildURL(self, path, params):
        """
        Combine base_url + path + params
        """
        q = path
        if params:
            q += '?'
            first = False
            for k, v in params.items():
                if first: q += '&'
                else: first = True
                q += k + '=' + str(v)
        return self.base_url + '/' + q.lstrip('/')

    def perform_request(self, method:str='GET', url:str="", **kwargs) -> Dict:
        """
        Perform the actual request, returns a dict of
            error: Bool
            error_text: str '' for no error
            data: Response.json(), None on error
        """
        response = dict(data=None)
        try:
            r = self.session.request(method, url, **kwargs)
            if r.status_code == 200:
                response["data"] = r.json()
            else: 
                response.update({'data':None,'error':True,'error_text':'Code: {}, Message: {}'.format(r.status_code,r.text)})
        except JSONDecodeError as json_error:
            response.update({'data':None,'error':True,'error_text':'JSONDecodeError: '.format(json_error)})
        except Exception as other_error:
            response.update({'data':None,'error':True,'error_text':'Exception: {}'.format(other_error)})
        return response


    def fetchOhlcv(self,    symbol:str, 
                            timeframe: str = '1m',
                            since: str = '',
                            limit: int = 100,
                            start_time: str = None,
                            end_time: str = None
                  ) -> DataFrame:
        """
        Fetch OHLCV data as pandas DataFrame
        """
        raise Error(-1, 'fetchOhlcv must be implemented in derived class') 

    def to_milliseconds(self, datestr):
        epoch = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
        d     = datetime.fromisoformat(datestr)
        if d.tzinfo is None or d.tzinfo.utcoffset(d) is None: d = d.replace(tzinfo=pytz.utc)
        return int((d - epoch).total_seconds() * 1000.0)



