"""
    Filename    :   error.py - Error handling
    Part of     :   pyOHLCV 1.0.04
    By          :   Emmanuel Adigun (emmanuel@zignal.net)
    Date        :   01 July 2022
"""

class Error(Exception):
    def __init__(self, code, message):
        self.code    = code
        self.message = message