import numpy as np
import pandas as pd
import pytest

from pricing_library.market_data import MarketData


def test_get_historical_vol_without_yfinance_call():
    data = MarketData("AAPL")

    fake_history = pd.DataFrame(
        {
            "Close": [100, 102, 101, 105, 107, 106, 110]
        }
    )

    data.get_history = lambda period="1y": fake_history

    close_price = fake_history["Close"]
    log_return = np.log(close_price / close_price.shift(1)).dropna()
    expected_vol = log_return.std() * np.sqrt(252)

    assert data.get_historical_vol("1y") == pytest.approx(expected_vol)