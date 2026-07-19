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