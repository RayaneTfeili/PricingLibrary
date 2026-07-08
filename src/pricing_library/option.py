class Option():
    def __init__(self, option_type: str, strike: float, maturity: float):
        self.option_type = option_type
        self.strike = strike 
        self.maturity = maturity 
     
        self.option_type = option_type.lower() 

        if self.option_type not in {"call","put"}:
            raise ValueError("Option type must be a call or a put")
        if self.strike <= 0:
            raise ValueError("Strike must be positive")
        if self.maturity <=0:
            raise ValueError("Maturity must be positive")
    def is_call(self):
        return self.option_type == "call"
    def is_put(self):
        return self.option_type =="put"
        
    def payoff(self, UP_final : float):
        if self.option_type =="call":
            return max(UP_final - self.strike,0)
        else:
            return max(self.strike - UP_final,0)
        
    def  __repr__(self):
        return (f"Option(type = {self.option_type}, strike = {self.strike}, maturity = {self.maturity})") 
    
    
class VanillaOption(Option):
    def __init__(self, option_type: str, strike: float, maturity: float):
        super().__init__(option_type, strike, maturity)
        if strike <= 0:
            raise ValueError("strike must be positive")

        self.strike = float(strike)

    def payoff(self, final_underlying_price: float):
        if final_underlying_price < 0:
            raise ValueError("Underlying price must be positive")

        if self.is_call():
            return max(final_underlying_price - self.strike, 0.0)

        return max(self.strike - final_underlying_price, 0.0)

    def __repr__(self) -> str:
        return (f"VanillaOption(type={self.option_type!r}, "f"strike={self.strike}, maturity={self.maturity})")