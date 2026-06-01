import pandas as pd
import pytest

from strategies.sma_crossover import (
    SMACrossoverStrategy,
)


class TestSMACrossoverStrategy:

    def test_strategy_metadata(self):

        strategy = SMACrossoverStrategy()

        assert strategy.name == "SMA_Crossover"

        assert strategy.parameters == {
            "fast_window": 20,
            "slow_window": 50,
        }

    def test_invalid_fast_window(self):

        with pytest.raises(ValueError):
            SMACrossoverStrategy(
                fast_window=0,
                slow_window=50,
            )

    def test_invalid_slow_window(self):

        with pytest.raises(ValueError):
            SMACrossoverStrategy(
                fast_window=20,
                slow_window=0,
            )

    def test_fast_window_must_be_smaller(self):

        with pytest.raises(ValueError):
            SMACrossoverStrategy(
                fast_window=50,
                slow_window=20,
            )

    def test_missing_close_column(self):

        strategy = SMACrossoverStrategy()

        df = pd.DataFrame(
            {
                "Open": [1, 2, 3]
            }
        )

        with pytest.raises(ValueError):
            strategy.generate_signals(df)

    def test_empty_dataframe(self):

        strategy = SMACrossoverStrategy()

        df = pd.DataFrame(
            {
                "Close": []
            }
        )

        result = strategy.generate_signals(df)

        assert "Signal" in result.columns

    def test_signal_column_created(self):

        strategy = SMACrossoverStrategy()

        df = pd.DataFrame(
            {
                "Close": range(1, 101)
            }
        )

        result = strategy.generate_signals(df)

        assert "Signal" in result.columns
        assert "SMA20" in result.columns
        assert "SMA50" in result.columns

    def test_input_not_modified(self):

        strategy = SMACrossoverStrategy()

        df = pd.DataFrame(
            {
                "Close": range(1, 101)
            }
        )

        original_columns = list(df.columns)

        strategy.generate_signals(df)

        assert list(df.columns) == original_columns

    def test_bullish_signal_generated(self):

        strategy = SMACrossoverStrategy()

        df = pd.DataFrame(
            {
                "Close": range(1, 101)
            }
        )

        result = strategy.generate_signals(df)

        assert result.iloc[-1]["Signal"] == 1

    def test_bearish_signal_generated(self):

        strategy = SMACrossoverStrategy()

        df = pd.DataFrame(
            {
                "Close": range(100, 0, -1)
            }
        )

        result = strategy.generate_signals(df)

        assert result.iloc[-1]["Signal"] == 0

    def test_equal_sma_produces_zero_signal(self):

        strategy = SMACrossoverStrategy()

        df = pd.DataFrame(
            {
                "Close": [100] * 100
            }
        )

        result = strategy.generate_signals(df)

        assert result.iloc[-1]["Signal"] == 0

    def test_signal_is_integer(self):

        strategy = SMACrossoverStrategy()

        df = pd.DataFrame(
            {
                "Close": range(1, 101)
            }
        )

        result = strategy.generate_signals(df)

        assert pd.api.types.is_integer_dtype(
            result["Signal"]
        )

    def test_signal_contains_only_binary_values(self):

        strategy = SMACrossoverStrategy()

        df = pd.DataFrame(
            {
                "Close": range(1, 101)
            }
        )

        result = strategy.generate_signals(df)

        assert set(
            result["Signal"].unique()
        ).issubset({0, 1})