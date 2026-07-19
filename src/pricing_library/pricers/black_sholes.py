from .base import BasePricer
from ..option import VanillaOption
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq

class BSPricer(BasePricer):
    def __init__(self,option : VanillaOption, spot_price : float, risk_free_rate : float, volatility : float):
        super().__init__(option = option, spot_price = spot_price, risk_free_rate = risk_free_rate, volatility = volatility)
    
    def _parameters(self):
        return self.spot_price, self.option.strike, self.option.maturity, self.risk_free_rate, self.volatility
    def _d1(self):
        
        S, K, T, r, vol = self._parameters()
        return (np.log(S / K) + (r + 0.5 * vol**2) * T) / (vol * np.sqrt(T))
    def _d2(self):
        S, K, T, r, vol = self._parameters()
        return self._d1() - vol * np.sqrt(T)
    def price(self):
        S, K,T,r,vol = self._parameters()
        d1 = self._d1()
        d2 = self._d2()
        if self.option.option_type == 'call':
            price = S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
        elif self.option.option_type == 'put':
            price = K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)  
        else: 
            raise ValueError("Option must be a call or a put")
        return np.round(price,2) 
    
    def implied_vol(self,market_price : float):
        def find(vol):
            pricer = BSPricer(option = self.option, spot_price = self.spot_price,risk_free_rate = self.risk_free_rate, volatility = vol)
            return pricer.price() - market_price 
        try:
            return brentq(find,0.001,1.0,maxiter = 1000)
        except ValueError:
            return brentq(find,0.001,3.0,maxiter = 1000)
    def delta(self):
        d1 = self._d1()
        return norm.cdf(d1) if self.option.is_call() else norm.cdf(d1) -1 

    def gamma(self):
        d1 = self._d1()
        S,K,T,r,vol = self._parameters()
        return norm.pdf(d1)/(S*vol*np.sqrt(T))
    
    def vega(self):
        d1 = self._d1()
        S,K,T,r,vol = self._parameters()
        return S*np.sqrt(T)*norm.pdf(d1)
    
    def theta(self):
        d2 = self._d2()
        S,K,T,r,vol = self._parameters()
        d1= self._d1()
        return (-S*norm.pdf(d1)*vol)/(2*np.sqrt(T)) - r *K*np.exp(-r*T)*norm.cdf(d2) if self.option.is_call() else (-S*norm.pdf(d1)*vol)/(2*np.sqrt(T)) + r *K*np.exp(-r*T)*norm.cdf(-d2)
    def rho(self):
        d2 = self._d2()
        S,K,T,r,vol = self._parameters()
        return K*T*np.exp(-r*T)*norm.cdf(d2) if self.option.is_call() else -K*T*np.exp(-r*T)*norm.cdf(-d2)

    
