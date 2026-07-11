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

    def __repr__(self):
        return (f"VanillaOption(type={self.option_type!r}, "f"strike={self.strike}, maturity={self.maturity})")
    

class AmericanOption(VanillaOption):
    def __repr__(self):
        return (f"AmericanOption(type={self.option_type!r}, "f"strike={self.strike}, maturity={self.maturity})")
    
class AsianOption(Option):
    def __init__(self,option_type : str, strike : float, maturity : float, averaging_method : str):
        super().__init__(option_type, strike,maturity)  
        self.averaging_method = averaging_method.lower()
        if self.averaging_method not in {"arithmetic", "geometric"}:
            raise ValueError("Averaging must be arithmetic or geometric")
        
    def __repr__(self):
        return (f"AsianOption(type={self.option_type!r}, "f"strike={self.strike}, maturity={self.maturity}, averaging_method={self.averaging_method})")
    
class BarrierOption(Option):
    def __init__(self,option_type : str, strike : float, maturity : float, barrier_type : str, barrier_level : float):
        super().__init__(option_type,strike,maturity)
        self.barrier_type = barrier_type.lower()
        self.barrier_level = barrier_level 
        if self.barrier_type not in {"up-and-in", "up-and-out", "down-and-in", "down-and-out"}:
            raise ValueError("Enter a valid barrier type  : up-and-in,up-and-out,down-and-in, down-and-out")

class SwingOption(Option):
    def __init__(self,option_type : str, strike : float, maturity : float, number_of_exercises : int):
        super().__init__(option_type,strike,maturity)
        self.number_of_exercises = number_of_exercises
        if self.number_of_exercises <= 0:
            raise ValueError("Specify a valid number of exercises, it must be a positive number")