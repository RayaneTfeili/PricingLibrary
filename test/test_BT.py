import pytest

from pricing_library.option import AmericanOption
from pricing_library.pricers import BTPricer, MCPricer


def test_binomial_american_put_price():
    option = AmericanOption("put", 100, 1)

    pricer = BTPricer(option, 100, 0.05, 0.2, 500)

    assert pricer.price() == pytest.approx(6.09, abs=0.05)


def test_binomial_vs_longstaff_schwartz_put():
    option = AmericanOption("put", 100, 1)

    bt = BTPricer(option, 100, 0.05, 0.2, 500)
    mc = MCPricer(option, 100, 0.05, 0.2, 100_000, 100, 42)

    assert mc.price() == pytest.approx(bt.price(), abs=0.4)