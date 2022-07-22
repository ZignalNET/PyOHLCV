"""
    Filename    :   luno.py - LUNO
    Part of     :   pyOHLCV
    By          :   Emmanuel Adigun (emmanuel@zignal.net)
    Date        :   01 July 2022
"""
from ..base import Base
class Luno(Base):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        