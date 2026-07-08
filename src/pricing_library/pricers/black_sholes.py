from .base import BasePricer
from ..option import VanillaOption 
from scipy.stats import norm

class BlackSholesPricer(BasePricer):
    def __init__(self,option : VanillaOption, spot_price : float, risk_free_rate : float, volatility : float):
        super().__init__(option = option, spot_price = spot_price, risk_free_rate = risk_free_rate, volatility = volatility)
    
    def price(self):
        pass 