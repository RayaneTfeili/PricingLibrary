import yfinance as yf 
import numpy as np 

class MarketData:
    def __init__(self,ticker : str):
        self.ticker = ticker 
        if self.ticker == "" or not isinstance(self.ticker, str):
            raise ValueError("Ticker must be a non empty string")
        else:
            self.data = yf.Ticker(self.ticker)

    def get_history(self, period : str):
        return self.data.history(period) 
    
    def get_price_range(self,period : str):
        history = self.get_history(period)
        return {"highest" : float(np.round(history['High'].max(),2)), "lowest" : float(np.round(history['Low'].min(),2)),}
    
    def get_price_latest(self):
        history =self.get_history(period = "3d")
        latest_price = history.iloc[-1]
        return {"close" : float(np.round(latest_price['Close'],2)),"open" : float(np.round(latest_price['Open'],2)),
                "highest" : float(np.round(latest_price['High'],2)),"lowest" : float(np.round(latest_price['Low'],2)),}
    
