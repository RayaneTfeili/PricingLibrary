from .base import BasePricer
from ..option import VanillaOption 
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
        sigma = self.volatility
        if self.option.option_type == 'call':
            d1 = (np.log(S/K) + (r+0.5*sigma**2)*T)/(sigma*np.sqrt(T))
            d2 = d1 - sigma*np.sqrt(T)
            price = S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
        elif self.option.option_type == 'put':
            d1 = (np.log(S/K) + (r+0.5*sigma**2)*T)/(sigma*np.sqrt(T))
            d2 = d1 - sigma*np.sqrt(T)
            price = K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)  
        else: 
            raise ValueError("Option must be a call or a put")
        return np.round(price,2) 