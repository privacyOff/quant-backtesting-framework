from typing import Any

import pandas as pd

from strategies.base_strategy import BaseStrategy


class SMACrossoverStrategy(BaseStrategy):
    """
    Simple Moving Average Crossover Strategy.

    Signal Logic
    ------------
    Signal = 1 when SMA_fast > SMA_slow
    Signal = 0 otherwise

    Long-only strategy.
    """

    def __init__(
        self,
        fast_window: int = 20,
        slow_window: int = 50,
    ):
        if fast_window <= 0:
            raise ValueError(
                "fast_window must be greater than 0."
            )

        if slow_window <= 0:
            raise ValueError(
                "slow_window must be greater than 0."
            )

        if fast_window >= slow_window:
            raise ValueError(
                "fast_window must be smaller than slow_window."
            )

        super().__init__(
            name="SMA_Crossover",
            parameters={
                "fast_window": fast_window,
                "slow_window": slow_window,
            },
        )

        self.fast_window = fast_window
        self.slow_window = slow_window

    def generate_signals(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:

        if "Close" not in data.columns:
            raise ValueError(
                "Close column not found in DataFrame."
            )

        result = data.copy()

        fast_col = f"SMA{self.fast_window}"
        slow_col = f"SMA{self.slow_window}"

        result[fast_col] = (
            result["Close"]
            .rolling(window=self.fast_window)
            .mean()
        )

        result[slow_col] = (
            result["Close"]
            .rolling(window=self.slow_window)
            .mean()
        )

        result["Signal"] = 0

        result.loc[
            result[fast_col] > result[slow_col],
            "Signal",
        ] = 1

        result["Signal"] = (
            result["Signal"]
            .fillna(0)
            .astype(int)
        )

        return result