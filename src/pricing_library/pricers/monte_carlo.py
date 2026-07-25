import numpy as np 
from scipy.stats import norm 
from .base import BasePricer 
from ..option import VanillaOption,AsianOption,BarrierOption, AmericanOption, SwingOption

class MCPricer(BasePricer):
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
    def path_antithetic(self):
        T = self.option.maturity 
        S0 = self.spot_price 
        R = self.risk_free_rate 
        vol = self.volatility 
        dt = T/self.nums_step 
        rng = np.random.default_rng(self.seeds)
        path1 = np.zeros([self.num_simulations, self.nums_step+1])
        path2 = np.zeros([self.num_simulations, self.nums_step+1])
        path1[:,0] = S0
        path2[:,0]= S0 
        for j in range(1,self.nums_step+1):
            z=  rng.standard_normal(self.num_simulations)
            path1[:,j] = path1[:,j-1] * np.exp(R-(vol**2)/2 * dt + vol *np.sqrt(dt)* z) 
            path2[:,j] = path2[:,j-1] * np.exp(R-(vol**2)/2 * dt + vol *np.sqrt(dt)* -z)
        return path1,path2 
    def payoff_from_path(self,path):
        if isinstance(self.option, AmericanOption):
            raise TypeError("We are using Long-Scharwtz method for the american option")
        if isinstance(self.option, AsianOption):
            paths = self.path()
            if self.option.averaging_method == "arithmetic":
                average_prices = np.mean(paths[:, 1:], axis=1)
            else:
                average_prices = np.exp(np.mean(np.log(paths[:, 1:]), axis=1))
            payoffs = np.maximum(average_prices - self.option.strike, 0) if self.option.is_call() else np.maximum(self.option.strike - average_prices, 0)
            return payoffs
        if isinstance(self.option, BarrierOption):
            paths = self.path()
            final_prices = paths[:, -1]
            if self.option.barrier_type == "up-and-in":
                barrier_hit = np.any(paths[:, 1:] >= self.option.barrier_level, axis=1)
                active = barrier_hit
            elif self.option.barrier_type == "up-and-out":
                barrier_hit = np.any(paths[:, 1:] >= self.option.barrier_level, axis=1)
                active = ~barrier_hit
            elif self.option.barrier_type == "down-and-in":
                barrier_hit = np.any(paths[:, 1:] <= self.option.barrier_level, axis=1)
                active = barrier_hit
            else:
                barrier_hit = np.any(paths[:, 1:] <= self.option.barrier_level, axis=1)
                active = ~barrier_hit
            payoffs = np.maximum(final_prices - self.option.strike, 0) if self.option.is_call() else np.maximum(self.option.strike - final_prices, 0)
            payoffs = np.where(active, payoffs, 0)
            return payoffs 
        if isinstance(self.option, VanillaOption):
            paths = self.path()
            final_prices = paths[:, -1]
            payoffs = np.maximum(final_prices - self.option.strike, 0) if self.option.is_call() else np.maximum(self.option.strike - final_prices, 0)
            return payoffs 
        raise TypeError("Swing Option coming in the futur, when I have more time")
    
    def discounted_payoffs(self):
        paths = self.path()
        payoff = self.payoff_from_path(paths)
        return np.exp(-self.risk_free_rate*self.option.maturity)*payoff 
    def discounted_payoffs_antithetic(self):
        path1,path2 = self.path_antithetic()
        payoff1 = self.payoff_from_path(path1)
        payoff2 = self.payoff_from_path(path2)
        payoff_antithetic = 0.5*(payoff1+payoff2)
        return np.exp(-self.risk_free_rate*self.option.maturity)*payoff_antithetic
        

    def _price_american(self):
            paths = self.path()
            dt = self.option.maturity / self.nums_step
            discount_factor = np.exp(-self.risk_free_rate * dt)
            payoffs = np.maximum(paths[:, -1] - self.option.strike, 0) if self.option.is_call() else np.maximum(self.option.strike - paths[:, -1], 0)
            for t in range(self.nums_step - 1, 0, -1):
                payoffs = payoffs * discount_factor
                immediate_exercise = np.maximum(paths[:, t] - self.option.strike, 0) if self.option.is_call() else np.maximum(self.option.strike - paths[:, t], 0)
                ITM = immediate_exercise > 0
                X = paths[ITM, t]
                Y = payoffs[ITM]
                coeffs = np.polyfit(X, Y, deg=2)
                continuation_value = np.polyval(coeffs, X)
                exercise_now = immediate_exercise[ITM] > continuation_value
                payoffs[ITM] = np.where(exercise_now,immediate_exercise[ITM],payoffs[ITM],)

            return np.mean(payoffs)
    def price(self):
        if isinstance(self.option,AmericanOption):
            return self._price_american()
        discounted_payoff= self.discounted_payoffs()
        return np.mean(discounted_payoff)
    def price_antithetic(self):
        if isinstance(self.option,AmericanOption):
            return self._price_american()
        discounted_payoff = self.discounted_payoffs_antithetic()
        return np.mean(discounted_payoff)
    def IC(self, level : float):
        disct_payoff = self.discounted_payoffs()
        price = np.mean(disct_payoff)
        error = np.std(disct_payoff, ddof = 1) /np.sqrt(self.num_simulations)
        alpha = 1 - level
        z = norm.ppf(1-alpha/2)
        return [price - error * z, price + error * z]
    def IC_antithetic(self,level : float):
        disct_payoff = self.discounted_payoffs_antithetic()
        price = np.mean(disct_payoff)
        error = np.std(disct_payoff, ddof = 1)/np.sqrt(self.num_simulations)
        alpha = 1-level 
        z = norm.ppf(1-alpha/2)
        return [price - error * z, price + error*z]
    
    def delta(self, h : float = 0.01):
        bump_up = MCPricer(self.option, self.spot_price+h, self.risk_free_rate,self.volatility, self.num_simulations, self.nums_step,self.seeds).price()
        bump_down =  MCPricer(self.option, self.spot_price-h, self.risk_free_rate,self.volatility, self.num_simulations, self.nums_step,self.seeds).price()
        return (bump_up - bump_down)/(2*h) 

    def gamma(self, h:float = 0.01):
        bump_up = MCPricer(self.option, self.spot_price+h, self.risk_free_rate,self.volatility, self.num_simulations, self.nums_step,self.seeds).price()
        bump_down =  MCPricer(self.option, self.spot_price-h, self.risk_free_rate,self.volatility, self.num_simulations, self.nums_step,self.seeds).price()
        in_between = MCPricer(self.option, self.spot_price, self.risk_free_rate,self.volatility, self.num_simulations, self.nums_step,self.seeds).price()
        return (bump_up-2*in_between  + bump_down)/h**2 
    
    def vega(self, h: float =0.01):
        bump_up = MCPricer(self.option, self.spot_price, self.risk_free_rate,self.volatility+h, self.num_simulations, self.nums_step,self.seeds).price()
        bump_down =  MCPricer(self.option, self.spot_price, self.risk_free_rate,self.volatility-h, self.num_simulations, self.nums_step,self.seeds).price()
        return (bump_up - bump_down)/(2*h)
    def rho(self,h : float =0.01):
        bump_up = MCPricer(self.option, self.spot_price, self.risk_free_rate+h,self.volatility, self.num_simulations, self.nums_step,self.seeds).price()
        bump_down = MCPricer(self.option, self.spot_price, self.risk_free_rate-h,self.volatility, self.num_simulations, self.nums_step,self.seeds).price()
        return (bump_up - bump_down)/(2*h)
 
    

