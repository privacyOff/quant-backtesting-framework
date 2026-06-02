import pandas as pd
import pytest

from strategies.momentum import (
    MomentumStrategy,
)


def sample_data():

    return pd.DataFrame(
        {
            "Close": [
                100,
                101,
                102,
                103,
                104,
                105,
                106,
                107,
                108,
                109,
            ]
        }
    )


def test_metadata():

    strategy = MomentumStrategy(
        lookback_period=20
    )

    assert (
        strategy.name
        == "Momentum"
    )

    assert (
        strategy.parameters[
            "lookback_period"
        ]
        == 20
    )


def test_invalid_lookback():

    with pytest.raises(
        ValueError
    ):
        MomentumStrategy(
            lookback_period=0
        )


def test_missing_close_column():

    strategy = (
        MomentumStrategy()
    )

    data = pd.DataFrame(
        {
            "Open": [1, 2, 3]
        }
    )

    with pytest.raises(
        ValueError
    ):
        strategy.generate_signals(
            data
        )


def test_empty_dataframe():

    strategy = (
        MomentumStrategy()
    )

    with pytest.raises(
        ValueError
    ):
        strategy.generate_signals(
            pd.DataFrame()
        )


def test_momentum_column_exists():

    strategy = (
        MomentumStrategy(
            lookback_period=3
        )
    )

    result = (
        strategy.generate_signals(
            sample_data()
        )
    )

    assert (
        "Momentum3"
        in result.columns
    )


def test_signal_column_exists():

    strategy = (
        MomentumStrategy(
            lookback_period=3
        )
    )

    result = (
        strategy.generate_signals(
            sample_data()
        )
    )

    assert (
        "Signal"
        in result.columns
    )


def test_positive_momentum_generates_long_signal():

    strategy = (
        MomentumStrategy(
            lookback_period=3
        )
    )

    result = (
        strategy.generate_signals(
            sample_data()
        )
    )

    assert (
        result["Signal"]
        .iloc[-1]
        == 1
    )


def test_negative_momentum_generates_flat_signal():

    data = pd.DataFrame(
        {
            "Close": [
                109,
                108,
                107,
                106,
                105,
                104,
                103,
                102,
                101,
                100,
            ]
        }
    )

    strategy = (
        MomentumStrategy(
            lookback_period=3
        )
    )

    result = (
        strategy.generate_signals(
            data
        )
    )

    assert (
        result["Signal"]
        .iloc[-1]
        == 0
    )


def test_input_dataframe_not_modified():

    strategy = (
        MomentumStrategy(
            lookback_period=3
        )
    )

    original = sample_data()

    data = original.copy()

    strategy.generate_signals(
        data
    )

    pd.testing.assert_frame_equal(
        original,
        data,
    )


def test_early_rows_have_zero_signal():

    strategy = (
        MomentumStrategy(
            lookback_period=5
        )
    )

    result = (
        strategy.generate_signals(
            sample_data()
        )
    )

    assert (
        result["Signal"]
        .iloc[:5]
        .eq(0)
        .all()
    )