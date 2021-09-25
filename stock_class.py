# This file creates a class for the each stock
class stock_info:
    def __init__(self, close, previous_close, market_cap, volume):
        self.close = close
        self.previous_close = previous_close
        self.market_cap =  market_cap
        self.volume = volume
    def get_close(self):
        return(self.close)
    def get_previous_close(self):
        return (self.previous_close) 
    def get_market_cap(self):
        return (self.market_cap) 
    def get_volume(self):
        return (self.volume)