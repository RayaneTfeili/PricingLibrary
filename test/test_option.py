import pytest

from pricing_library.option import (
    Option,
    VanillaOption,
    AmericanOption,
    AsianOption,
    BarrierOption,
    SwingOption,
)


def test_option_creation():
    option = Option("call", 100, 1)

    assert option.option_type == "call"
    assert option.strike == 100
    assert option.maturity == 1
    assert option.is_call()
    assert not option.is_put()


def test_invalid_option_type():
    with pytest.raises(ValueError):
        Option("bad_type", 100, 1)


def test_invalid_strike():
    with pytest.raises(ValueError):
        Option("call", -100, 1)


def test_invalid_maturity():
    with pytest.raises(ValueError):
        Option("call", 100, -1)


def test_vanilla_payoff_call():
    option = VanillaOption("call", 100, 1)

    assert option.payoff(120) == 20
    assert option.payoff(80) == 0


def test_vanilla_payoff_put():
    option = VanillaOption("put", 100, 1)

    assert option.payoff(80) == 20
    assert option.payoff(120) == 0


def test_american_is_vanilla():
    option = AmericanOption("put", 100, 1)

    assert isinstance(option, VanillaOption)
    assert option.payoff(80) == 20


def test_asian_option():
    option = AsianOption("call", 100, 1, "arithmetic")

    assert option.averaging_method == "arithmetic"


def test_invalid_asian_averaging():
    with pytest.raises(ValueError):
        AsianOption("call", 100, 1, "bad")


def test_barrier_option():
    option = BarrierOption("call", 100, 1, "up-and-out", 120)

    assert option.barrier_type == "up-and-out"
    assert option.barrier_level == 120


def test_swing_option():
    option = SwingOption("call", 100, 1, 5)

    assert option.number_of_exercises == 5