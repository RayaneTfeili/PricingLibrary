from .base import BasePricer 
import numpy as np 
from ..option import AmericanOption
class BTPricer(BasePricer):
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
    
    