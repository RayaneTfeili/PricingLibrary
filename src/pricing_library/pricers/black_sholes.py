from .base import BasePricer
from ..option import VanillaOption, AmericanOption, AsianOption, BarrierOption, SwingOption 
import numpy as np
from scipy.stats import norm

class BlackSholesVanillaPricer(BasePricer):
    def __init__(self,option : VanillaOption, spot_price : float, risk_free_rate : float, volatility : float):
        super().__init__(option = option, spot_price = spot_price, risk_free_rate = risk_free_rate, volatility = volatility)
    
    def price(self):
        S = self.spot_price
        K = self.option.strike
        T = self.option.maturity
        r = self.risk_free_rate
        vol = self.volatility
        if self.option.option_type == 'call':
            d1 = (np.log(S/K) + (r+0.5*vol**2)*T)/(vol*np.sqrt(T))
            d2 = d1 - vol*np.sqrt(T)
            price = S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
        elif self.option.option_type == 'put':
            d1 = (np.log(S/K) + (r+0.5*vol**2)*T)/(vol*np.sqrt(T))
            d2 = d1 - vol*np.sqrt(T)
            price = K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)  
        else: 
            raise ValueError("Option must be a call or a put")
        return np.round(price,2) 
    
class BinomialTreePricer(BasePricer):
    def __init__(self,option : AmericanOption, spot_price : float, risk_free_rate : float, volatility : float, num_steps : int):
        super().__init__(option = option, spot_price = spot_price, risk_free_rate = risk_free_rate, volatility = volatility)
        self.num_steps = num_steps

    def price(self) -> float:
        n = self.num_steps
        S0 = self.spot_price
        K = self.option.strike
        T = self.option.maturity
        r = self.risk_free_rate
        vol = self.volatility
        dt = T / n
        u = np.exp(vol * np.sqrt(dt))
        d = 1 / u
        p = (np.exp(r * dt)-d)/(u-d)
        j = np.arange(n + 1)
        stock_prices = S0 * (u ** j) * (d ** (n - j))
        if self.option.is_call():
            option_values = np.maximum(stock_prices - K, 0.0)
        else:
            option_values = np.maximum(K - stock_prices, 0.0)
        for step in range(n - 1, -1, -1):
            continuation_values = np.exp(-r*dt)*(p*option_values[1:]+(1 - p)*option_values[:-1])
            j = np.arange(step + 1)
            stock_prices = S0 * (u ** j) * (d ** (step - j))
            if self.option.is_call():
                exercise_values = np.maximum(stock_prices - K, 0.0)
            else:
                exercise_values = np.maximum(K - stock_prices, 0.0)
            option_values = np.maximum(continuation_values, exercise_values)
        return np.round(option_values[0], 2)
    
    