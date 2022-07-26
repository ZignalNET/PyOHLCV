"""
    Filename    :   __init__.py 
    Part of     :   pyOHLCV
    By          :   Emmanuel Adigun (emmanuel@zignal.net)
    Date        :   01 July 2022
"""
from .luno import Luno
from .binance import Binance
from .coinbasepro import CoinbasePro
from .kucoin import Kucoin

exchanges = [
                'Binance',
                'Coinbase Pro',
                'Luno',
                'Kucoin'
]