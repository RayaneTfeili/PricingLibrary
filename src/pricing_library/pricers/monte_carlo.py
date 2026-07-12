import numpy as np 
from .base import BasePricer 
from ..option import VanillaOption,AsianOption,BarrierOption, AmericanOption, SwingOption

class MonteCarloPricer(BasePricer):
    def __init__(self, option, spot_price : float, risk_free_rate : float, volatility : float, num_simulations : int, nums_step : int,seeds : int = 45):
        super().__init__(option = option, spot_price = spot_price, risk_free_rate = risk_free_rate, volatility = volatility)
        self.num_simulations = num_simulations 
        self.nums_step = nums_step
        self.seeds = seeds 
        
    def path(self):
        T = self.option.maturity 
        S0 = self.spot_price 
        R = self.risk_free_rate 
        vol = self.volatility 
        dt = T/self.nums_step 
        rng = np.random.default_rng(self.seeds)
        paths = np.zeros((self.num_simulations, self.nums_step +1))
        paths[:,0] = S0 
        for j in range(1,self.nums_step +1):
            z = rng.standard_normal(self.num_simulations)
            paths[:,j] = paths[:,j-1]*np.exp((R - 0.5*vol**2)*dt + vol*np.sqrt(dt)*z)
        return paths
    
    def price(self):
        if isinstance(self.option,VanillaOption):
            paths = self.path()
            final_prices = paths[:,-1]
            payoffs = np.maximum(final_prices - self.option.strike,0) if self.option.is_call() else np.maximum(self.option.strike -final_prices,0)
            discounted_payoff = np.exp(-self.risk_free_rate*self.option.maturity)*payoffs 
            return np.round(np.mean(discounted_payoff),2)
        
        if isinstance(self.option,AsianOption):
            paths = self.path()
            if self.option.averaging_method == "arithmetic":
                average_prices = np.mean(paths[:,1:],axis = 1)
            else:
                average_prices = np.exp(np.mean(np.log(paths[:,1:]),axis = 1))
            payoffs = np.maximum(average_prices - self.option.strike,0) if self.option.is_call() else np.maximum(self.option.strike - average_prices,0)
            discounted_payoff = np.exp(-self.risk_free_rate*self.option.maturity)*payoffs 
            return np.round(np.mean(discounted_payoff),2)
        
        if isinstance(self.option,BarrierOption): 
            paths = self.path()
            if self.option.barrier_type =="up-and-in":
                barrier_hit = np.any(paths[:,1:] >= self.option.barrier_level,axis = 1)
                final_prices = paths[:,-1]
                payoffs = np.where(barrier_hit,np.maximum(final_prices - self.option.strike,0) if self.option.is_call() else np.maximum(self.option.strike - final_prices,0),0)
                discounted_payoff = np.exp(-self.risk_free_rate*self.option.maturity)*payoffs
            elif self.option.barrier_type =="up-and-out":
                barrier_hit = np.any(paths[:,1:] >= self.option.barrier_level,axis = 1)
                final_prices = paths[:,-1]
                payoffs = np.where(~barrier_hit,np.maximum(final_prices - self.option.strike,0) if self.option.is_call() else np.maximum(self.option.strike - final_prices,0),0)
                discounted_payoff = np.exp(-self.risk_free_rate*self.option.maturity)*payoffs
                discounted_payoff = np.exp(-self.risk_free_rate*self.option.maturity)*payoffs
            elif self.option.barrier_type =="down-and-in":
                barrier_hit = np.any(paths[:,1:] <= self.option.barrier_level,axis = 1)
                final_prices = paths[:,-1]
                payoffs = np.where(barrier_hit,np.maximum(final_prices - self.option.strike,0) if self.option.is_call() else np.maximum(self.option.strike - final_prices,0),0)
                discounted_payoff = np.exp(-self.risk_free_rate*self.option.maturity)*payoffs
            else:
                barrier_hit = np.any(paths[:,1:] <= self.option.barrier_level,axis = 1)
                final_prices = paths[:,-1]
                payoffs = np.where(~barrier_hit,np.maximum(final_prices - self.option.strike,0) if self.option.is_call() else np.maximum(self.option.strike - final_prices,0),0)
                discounted_payoff = np.exp(-self.risk_free_rate*self.option.maturity)*payoffs
            return np.round(np.mean(discounted_payoff),2) 
        if isinstance(self.option,AmericanOption):
            paths = self.path()
            if self.option.is_call():
                payoffs = np.maximum(paths[:,-1] - self.option.strike,0)
            if self.option.is_put():
                payoffs = np.maximum(self.option.strike - paths[:,-1],0) 
            for t in range(self.nums_step-1,0,-1):
                immediate_exercise = np.maximum(paths[:,t] - self.option.strike,0) if self.option.is_call() else np.maximum(self.option.strike - paths[:,t],0)
                ITM = immediate_exercise > 0 
                X = paths[ITM,t]
                Y = payoffs[ITM]*np.exp(-self.risk_free_rate*(self.option.maturity/self.nums_step))
                coeffs = np.polyfit(X, Y, deg=2)
                continuation_value = np.polyval(coeffs, X)

                exercise_now = immediate_exercise[ITM] > continuation_value

                payoffs[ITM] = np.where(exercise_now,immediate_exercise[ITM],Y)

            return np.round(np.mean(payoffs),2)
      
        else: 
            raise TypeError("Now I only have implemented MC for Vanilla, Asian and Barrier options. New options coming soon")

        if isinstance(self.option,SwingOption):
            pass 