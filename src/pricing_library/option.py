class Option():
    def __init__(self, option_type: str, strike: float, maturity: float, underlying_price: float, volatility: float, risk_free_rate: float):
        self.option_type = option_type
        self.strike = strike 
        self.maturity = maturity 
        self.up = underlying_price 
        self.vol = volatility 
        self.rfr = risk_free_rate 
        self.option_type = option_type.lower() 

        if self.option_type not in {"call","put"}:
            raise ValueError("Option type must be a call or a put")
        if self.strike <= 0:
            raise ValueError("Strike must be positive")
        if self.maturity <=0:
            raise ValueError("Maturity must be positive")
        if self.vol <=0:
            raise ValueError("Volatility must be positive")
        if self.rfr < 0:
            raise ValueError("Risk-free rate must be non-negative") 
        if self.up <=0:
            raise ValueError("Underlying price must be positive")
        
    def payoff(self, UP_final : float):
        if self.option_type =="call":
            return max(UP_final - self.strike,0)
        else:
            return max(self.strike - UP_final,0)
        
    def  __repr__(self):
        return (f"Option(type = {self.option_type}, strike = {self.strike}, maturity = {self.maturity}"
                f"underlying_price = {self.up} , volatility = {self.vol}, risk_free_rate = {self.rfr})") 
    
