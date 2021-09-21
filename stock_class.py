# This file creates a class for the each stock
class stock_info:
    def __init__(self, symbol, close, last_close, market_cap, volume):
        self.symbol = symbol
        self.close = close
        self.last_close = last_close
        self.market_cap =  market_cap
        self.volume = volume
    def get_info(self):
        print(self.symbol + '\t' +
              self.close + '\t' +
              self.last_close + '\t' +
              self.market_cap + '\t' +
              self.volume)