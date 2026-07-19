# PricingLibrary

PricingLibrary is library option pricing. This project is build in Python and when I'll have the time in C# or C++ 

## Main features

1. Option contract classes
2. Black-Scholes pricing
3. Monte Carlo pricing
4. Binomial tree pricing
5. Longstaff-Schwartz pricing for American options
6. Analytical Greeks for Black-Scholes
7. Numerical Greeks using Monte Carlo
8. Historical volatility 
9. Implied volatility
10. Unit tests with pytest

## Installation

This project uses `uv` for dependency and virtual environment management.

`uv` is used to create the Python environment, install dependencies, and run commands inside the project environment.

### Install uv on Windows

Open PowerShell and run:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After installation, restart PowerShell and check that uv is installed:

```powershell
uv version
```

### Clone the repository

```powershell
git clone <https://github.com/RayaneTfeili/PricingLibrary>
cd PricingLibrary
```

### Install dependencies

From the root of the project, run:

```powershell
uv sync
```

This command installs the dependencies defined in `pyproject.toml` and uses the versions locked in `uv.lock`.

### Run Python with uv

```powershell
uv run python
```

### Run the tests

```powershell
uv run pytest
```

## Repository structure

```text
PricingLibrary
├── src
│   └── pricing_library
│       ├── __init__.py
│       ├── option.py
│       ├── market_data.py
│       ├── models.py
│       └── pricers
│           ├── __init__.py
│           ├── base.py
│           ├── black_sholes.py
│           ├── binomial.py
│           └── monte_carlo.py
│
├── test
│   ├── test_BS.py
│   ├── test_BT.py
│   ├── test_MC.py
│   ├── test_market_data.py
│   └── test_option.py
│
├── pyproject.toml
├── uv.lock
├── README.md
└── .gitignore
```

## Project design

The project is organized around two main ideas.

First, option contracts are represented by Python classes. Each class describes the structure of a financial contract.

Second, pricing methods are represented by pricer classes. Each pricer receives an option and market parameters, then computes a price.

The idea behind this separation is to use different methods to price the same option contract (e.g for American option, one can use BTPricer or MCPricer classes)

## Option classes

The option classes are defined in `option.py`.

### Option

`Option` is the base class for the option contracts.

It stores the common contract information currently used in the project:

```python
option_type
strike
maturity
```

The `option_type` can be:

```text
call
put
```

The class also provides helper methods:

```python
is_call()
is_put()
payoff()
```

The payoff represents the value of the option at exercise.

For a call option:

```text
max(S - K, 0)
```

For a put option:

```text
max(K - S, 0)
```

### VanillaOption

`VanillaOption` represents a standard European vanilla option.

It has:

```text
option type
strike
maturity
payoff
```

### AmericanOption

`AmericanOption` inherits from `VanillaOption`.

Currently in my code, there are two ways to compute the pricer of an American Option 

```text
binomial tree
Longstaff-Schwartz Monte Carlo
```


### AsianOption

`AsianOption` represents an option whose payoff depends on the average price of the underlying asset.

The average can be:

```text
arithmetic
geometric
```

For an arithmetic Asian call, the payoff is based on:

```text
max(average price - strike, 0)
```

For an arithmetic Asian put, the payoff is based on:

```text
max(strike - average price, 0)
```

Asian options are priced in this project using Monte Carlo simulation.

### BarrierOption

`BarrierOption` represents an option activated or deactivated when the underlying price reaches a barrier level.

The supported barrier types are:

```text
up-and-in
up-and-out
down-and-in
down-and-out
```

Barrier options are path-dependent. This means the payoff depends not only on the final price, but also on the path followed by the underlying asset.

They are priced in this project using Monte Carlo simulation.

### SwingOption

`SwingOption` represents an option with several possible exercise rights.

Not implemented for now 

## MarketData

The `MarketData` class is defined in `market_data.py`.

It is used to retrieve historical market data, usually with `yfinance`.

Typical usage:

```python
from pricing_library.market_data import MarketData

data = MarketData("AAPL")

history = data.get_history(period="1y")
spot = data.get_spot_price()
vol = data.get_historical_vol(period="1y")
```

### Historical volatility

Historical volatility is computed from historical close prices.

The process is:

1. Retrieve historical close prices
2. Compute log returns
3. Compute the standard deviation of log returns
4. Annualize the result with the square root of 252

The formula is:

```text
historical volatility = std(log returns) * sqrt(252)
```


## Pricer classes

The pricer classes are located in `src/pricing_library/pricers`.

## BasePricer

`BasePricer` is the abstract parent class for the pricing classes.

It stores the common pricing inputs:

```python
option
spot_price
risk_free_rate
volatility
```

Every pricer must implement a `price()` method.

This gives the project a common interface. For example, every pricer can be used like this:

```python
price = pricer.price()
```

## BSPricer

`BSPricer` implements the Black-Scholes formula for vanilla European options.

It supports:

```text
call price
put price
analytical Greeks
implied volatility
```

Example:

```python
from pricing_library.option import VanillaOption
from pricing_library.pricers import BSPricer

option = VanillaOption("call", 100, 1)

pricer = BSPricer(
    option=option,
    spot_price=100,
    risk_free_rate=0.05,
    volatility=0.2,
)

print(pricer.price())
```

Expected result:

```text
around 10.45
```

### Black-Scholes Greeks

`BSPricer` includes analytical formulas for:

```text
delta
gamma
vega
theta
rho
```

Example:

```python
print(pricer.delta())
print(pricer.gamma())
print(pricer.vega())
print(pricer.theta())
print(pricer.rho())
```


### Implied volatility

`BSPricer` also includes an implied volatility method.

Implied volatility is the volatility that makes the Black-Scholes price equal to a market option price.

The idea is to solve:

```text
Black-Scholes price(volatility) = market price
```

Example:

```python
implied_vol = pricer.implied_vol(market_price=10.45)

print(implied_vol)
```


## MCPricer

`MCPricer` implements Monte Carlo pricing.

It simulates price paths using a geometric Brownian motion.

The simulated path follows the idea:

```text
current price
next simulated price
next simulated price
final simulated price
```

The Monte Carlo price is computed as:

```text
discounted average payoff
```

`MCPricer` supports:

```text
VanillaOption
AsianOption
BarrierOption
AmericanOption with Longstaff-Schwartz
```

Example with a vanilla option:

```python
from pricing_library.option import VanillaOption
from pricing_library.pricers import MCPricer

option = VanillaOption("call", 100, 1)

pricer = MCPricer(
    option,
    100,
    0.05,
    0.2,
    100000,
    252,
    42,
)

print(pricer.price())
```

The Monte Carlo price should be close to the Black-Scholes price for a vanilla European option.

### Monte Carlo Greeks

`MCPricer` computes Greeks numerically using bump and reprice.

For example, delta is approximated by changing the spot price slightly:

```text
delta = [Price(S + h) - Price(S - h)] / (2h)
```

The same idea is used for:

```text
delta
gamma
vega
rho
```


## BTPricer

`BTPricer` implements a binomial tree pricer for American options.

The binomial tree method works by building a price tree for the underlying asset.

At each node, the option value is the maximum between:

```text
continuation value
exercise value
```

This is why it is suitable for American options.

Example:

```python
from pricing_library.option import AmericanOption
from pricing_library.pricers import BTPricer

option = AmericanOption("put", 100, 1)

pricer = BTPricer(
    option,
    100,
    0.05,
    0.2,
    500,
)

print(pricer.price())
```

Expected result:

```text
around 6.09
```

## Longstaff-Schwartz for American options

The project also implements a Longstaff-Schwartz approach inside the Monte Carlo pricer for American options.

The idea is:

1. Simulate many price paths
2. Start from maturity
3. Move backward in time
4. Estimate continuation value using regression
5. Compare immediate exercise with continuation
6. Exercise if immediate exercise is better
7. Average discounted cashflows

This method is useful because it extends Monte Carlo to products with early exercise.

For an American put with:

```text
spot price = 100
strike = 100
risk free rate = 5 percent
volatility = 20 percent
maturity = 1 year
```

the Longstaff-Schwartz price should be close to the binomial tree price.

## Tests

The project uses pytest.

The tests check:

```text
option creation
invalid option inputs
payoff logic
Black-Scholes prices
Black-Scholes Greeks
implied volatility
Monte Carlo price against Black-Scholes
Monte Carlo Greeks against Black-Scholes
binomial tree pricing
Longstaff-Schwartz against binomial tree
historical volatility calculation
```

Run all tests with:

```powershell
uv run pytest
```

Current test suite:

```text
27 tests
27 passed
```

## Example workflow

```python
from pricing_library.option import VanillaOption
from pricing_library.pricers import BSPricer, MCPricer

option = VanillaOption("call", 100, 1)

bs = BSPricer(option, 100, 0.05, 0.2)
mc = MCPricer(option, 100, 0.05, 0.2, 100000, 252, 42)

print("Black-Scholes price:", bs.price())
print("Monte Carlo price:", mc.price())

print("Black-Scholes delta:", bs.delta())
print("Monte Carlo delta:", mc.delta())
```

## Current status

The project currently includes a working pricing framework with several pricing models and tests.

Implemented:

```text
Option contracts
Market data 
Black-Scholes pricing
Analytical Greeks
Implied volatility
Monte Carlo pricing
Monte Carlo Greeks
Binomial tree pricing
Longstaff-Schwartz for American options
Historical volatility
pytest 
```

Not implemented yet:

```text
Swing option pricing
Finite difference methods
Streamlit interface
More advanced volatility models
Calibration to market option chains
```

## Future improvements

Possible next steps:

```text
Add finite difference pricing
Add a complete SwingOption pricer
Add a Streamlit dashboard
Add option chain data
Add implied volatility surface construction
Improve documentation
Add more unit tests
```


