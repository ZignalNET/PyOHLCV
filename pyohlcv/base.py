"""
    Filename    :   base.py - Base file for exchanges
    Part of     :   pyOHLCV
    By          :   Emmanuel Adigun (emmanuel@zignal.net)
    Date        :   01 July 2022
"""

class Base:
    def __init__(self,**kwargs):
        self.api_key    = kwargs["api_key"]
        self.api_secret = kwargs["api_secret"]
