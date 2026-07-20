import pytest

from pricing_library.option import VanillaOption, AsianOption, BarrierOption, AmericanOption
from pricing_library.pricers import MCPricer, BSPricer


def test_mc_vanilla_close_to_bs():
    option = VanillaOption("call", 100, 1)

    bs = BSPricer(option, 100, 0.05, 0.2)
    mc = MCPricer(option, 100, 0.05, 0.2, 100_000, 252, 42)

    assert mc.price() == pytest.approx(bs.price(), abs=0.25)


def test_mc_delta_close_to_bs():
    option = VanillaOption("call", 100, 1)

    bs = BSPricer(option, 100, 0.05, 0.2)
    mc = MCPricer(option, 100, 0.05, 0.2, 100_000, 252, 42)

    assert mc.delta() == pytest.approx(bs.delta(), abs=0.03)


def test_mc_vega_close_to_bs():
    option = VanillaOption("call", 100, 1)

    bs = BSPricer(option, 100, 0.05, 0.2)
    mc = MCPricer(option, 100, 0.05, 0.2, 100_000, 252, 42)

    assert mc.vega() == pytest.approx(bs.vega(), abs=1.0)


def test_mc_asian_price_positive():
    option = AsianOption("call", 100, 1, "arithmetic")

    mc = MCPricer(option, 100, 0.05, 0.2, 50_000, 252, 42)

    assert mc.price() > 0


def test_mc_barrier_price_positive():
    option = BarrierOption("call", 100, 1, "up-and-out", 130)

    mc = MCPricer(option, 100, 0.05, 0.2, 50_000, 252, 42)

    assert mc.price() >= 0


def test_mc_american_put_price_positive():
    option = AmericanOption("put", 100, 1)

    mc = MCPricer(option, 100, 0.05, 0.2, 100_000, 100, 42)

    assert mc.price() > 0

def test_mc_confidence_interval_contains_price():
    option = VanillaOption("call", 100, 1)

    mc = MCPricer(option, 100, 0.05, 0.2, 100_000, 252, 42)

    lower, upper = mc.IC(0.95)
    price = mc.price()

    assert lower < price < upper

def test_mc_confidence_interval_width_decreases():
    option = VanillaOption("call", 100, 1)

    mc_small = MCPricer(option, 100, 0.05, 0.2, 10_000, 252, 42)
    mc_large = MCPricer(option, 100, 0.05, 0.2, 100_000, 252, 42)

    lower_small, upper_small = mc_small.IC(0.95)
    lower_large, upper_large = mc_large.IC(0.95)

    width_small = upper_small - lower_small
    width_large = upper_large - lower_large

    assert width_large < width_small

def test_mc_confidence_interval_99_is_wider_than_95():
    option = VanillaOption("call", 100, 1)

    mc = MCPricer(option, 100, 0.05, 0.2, 100_000, 252, 42)

    lower_95, upper_95 = mc.IC(0.95)
    lower_99, upper_99 = mc.IC(0.99)

    width_95 = upper_95 - lower_95
    width_99 = upper_99 - lower_99

    assert width_99 > width_95