from abc import ABC, abstractmethod
from ..option import Option

class BasePricer(ABC):
    def __init__(self, option: Option, spot_price: float, risk_free_rate: float, volatility: float):
        self.option = option
        self.spot_price = spot_price
        self.risk_free_rate = risk_free_rate
        self.volatility = volatility 
    
    @abstractmethod 
    def price(self):
        pass    
    