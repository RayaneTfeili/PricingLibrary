import pytest

from pricing_library.option import VanillaOption
from pricing_library.pricers import BSPricer


def test_bs_call_price():
    option = VanillaOption("call", 100, 1)
    pricer = BSPricer(option, 100, 0.05, 0.2)

    assert pricer.price() == pytest.approx(10.45, abs=0.01)


def test_bs_put_price():
    option = VanillaOption("put", 100, 1)
    pricer = BSPricer(option, 100, 0.05, 0.2)

    assert pricer.price() == pytest.approx(5.57, abs=0.01)


def test_bs_delta_call():
    option = VanillaOption("call", 100, 1)
    pricer = BSPricer(option, 100, 0.05, 0.2)

    assert pricer.delta() == pytest.approx(0.6368, abs=0.001)


def test_bs_gamma():
    option = VanillaOption("call", 100, 1)
    pricer = BSPricer(option, 100, 0.05, 0.2)

    assert pricer.gamma() == pytest.approx(0.01876, abs=0.001)


def test_bs_vega():
    option = VanillaOption("call", 100, 1)
    pricer = BSPricer(option, 100, 0.05, 0.2)

    assert pricer.vega() == pytest.approx(37.52, abs=0.1)


def test_bs_rho():
    option = VanillaOption("call", 100, 1)
    pricer = BSPricer(option, 100, 0.05, 0.2)

    assert pricer.rho() == pytest.approx(53.23, abs=0.1)


def test_implied_vol():
    option = VanillaOption("call", 100, 1)
    pricer = BSPricer(option, 100, 0.05, 0.2)

    implied_vol = pricer.implied_vol(10.45)

    assert implied_vol == pytest.approx(0.20, abs=0.01)