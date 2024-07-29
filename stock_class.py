# This file creates a class for the each stock
class stock_info:
    def __init__(self, 
                 name:str, 
                 close:float, 
                 previous_close:float, 
                 volume, 
                 market_cap:str):
        self.name = name
        self.close = close
        self.previous_close = previous_close
        self.volume = volume
        self.market_cap =  market_cap