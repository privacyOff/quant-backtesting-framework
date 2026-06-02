from typing import Dict

import pandas as pd

from strategies.base_strategy import BaseStrategy


class MomentumStrategy(BaseStrategy):
    """
    Long-only momentum strategy.

    Signal = 1 when:

        Close_t / Close_(t-lookback) - 1 > 0

    Signal = 0 otherwise.
    """

    def __init__(
        self,
        lookback_period: int = 20,
    ):

        if lookback_period <= 0:
            raise ValueError(
                "lookback_period must be > 0"
            )

        self.lookback_period = (
            lookback_period
        )

        self.name = "Momentum"

        self.parameters: Dict = {
            "lookback_period":
                lookback_period
        }

    def generate_signals(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:

        if data.empty:
            raise ValueError(
                "Input data cannot be empty"
            )

        if "Close" not in data.columns:
            raise ValueError(
                "Close column is required"
            )

        result = data.copy()

        momentum_col = (
            f"Momentum"
            f"{self.lookback_period}"
        )

        result[momentum_col] = (
            result["Close"]
            / result["Close"].shift(
                self.lookback_period
            )
            - 1
        )

        result["Signal"] = 0

        result.loc[
            result[momentum_col] > 0,
            "Signal",
        ] = 1

        result["Signal"] = (
            result["Signal"]
            .fillna(0)
            .astype(int)
        )

        return result