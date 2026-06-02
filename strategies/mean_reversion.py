from typing import Dict

import numpy as np
import pandas as pd

from strategies.base_strategy import BaseStrategy


class MeanReversionStrategy(BaseStrategy):
    """
    Long-only Z-score mean reversion strategy.

    Entry:
        ZScore < entry_threshold

    Exit:
        ZScore >= exit_threshold
    """

    def __init__(
        self,
        lookback_period: int = 20,
        entry_threshold: float = -2.0,
        exit_threshold: float = 0.0,
    ):

        if lookback_period <= 0:
            raise ValueError(
                "lookback_period must be > 0"
            )

        if entry_threshold >= exit_threshold:
            raise ValueError(
                "entry_threshold must be less than "
                "exit_threshold"
            )

        self.lookback_period = lookback_period
        self.entry_threshold = entry_threshold
        self.exit_threshold = exit_threshold

        self.name = "MeanReversion"

        self.parameters: Dict = {
            "lookback_period": lookback_period,
            "entry_threshold": entry_threshold,
            "exit_threshold": exit_threshold,
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

        sma_col = (
            f"SMA{self.lookback_period}"
        )

        std_col = (
            f"STD{self.lookback_period}"
        )

        zscore_col = (
            f"ZScore{self.lookback_period}"
        )

        result[sma_col] = (
            result["Close"]
            .rolling(
                window=self.lookback_period,
                min_periods=self.lookback_period,
            )
            .mean()
        )

        result[std_col] = (
            result["Close"]
            .rolling(
                window=self.lookback_period,
                min_periods=self.lookback_period,
            )
            .std()
        )

        result[zscore_col] = (
            (
                result["Close"]
                - result[sma_col]
            )
            / result[std_col]
        )

        result[zscore_col] = (
            result[zscore_col]
            .replace(
                [np.inf, -np.inf],
                np.nan,
            )
        )

        result["Signal"] = 0

        in_position = False

        for idx in result.index:

            zscore = result.at[
                idx,
                zscore_col,
            ]

            if pd.isna(zscore):
                result.at[
                    idx,
                    "Signal",
                ] = int(in_position)
                continue

            if (
                not in_position
                and zscore
                < self.entry_threshold
            ):

                in_position = True

            elif (
                in_position
                and zscore
                >= self.exit_threshold
            ):

                in_position = False

            result.at[
                idx,
                "Signal",
            ] = int(in_position)

        result["Signal"] = (
            result["Signal"]
            .fillna(0)
            .astype(int)
        )

        return result