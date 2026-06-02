import pandas as pd
import pytest

from strategies.mean_reversion import (
    MeanReversionStrategy,
)


def test_metadata():

    strategy = (
        MeanReversionStrategy()
    )

    assert (
        strategy.name
        == "MeanReversion"
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
        MeanReversionStrategy(
            lookback_period=0
        )


def test_invalid_thresholds():

    with pytest.raises(
        ValueError
    ):
        MeanReversionStrategy(
            entry_threshold=0,
            exit_threshold=0,
        )

    with pytest.raises(
        ValueError
    ):
        MeanReversionStrategy(
            entry_threshold=1,
            exit_threshold=0,
        )


def test_missing_close_column():

    strategy = (
        MeanReversionStrategy()
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
        MeanReversionStrategy()
    )

    with pytest.raises(
        ValueError
    ):
        strategy.generate_signals(
            pd.DataFrame()
        )


def test_indicator_columns_exist():

    strategy = (
        MeanReversionStrategy(
            lookback_period=3
        )
    )

    data = pd.DataFrame(
        {
            "Close": [
                100,
                100,
                100,
                90,
                100,
                110,
            ]
        }
    )

    result = (
        strategy.generate_signals(
            data
        )
    )

    assert "SMA3" in result.columns
    assert "STD3" in result.columns
    assert "ZScore3" in result.columns


def test_signal_column_exists():

    strategy = (
        MeanReversionStrategy(
            lookback_period=3
        )
    )

    data = pd.DataFrame(
        {
            "Close": [
                100,
                100,
                100,
                90,
                100,
                110,
            ]
        }
    )

    result = (
        strategy.generate_signals(
            data
        )
    )

    assert (
        "Signal"
        in result.columns
    )


def test_entry_logic():

    strategy = (
        MeanReversionStrategy(
            lookback_period=3,
            entry_threshold=-1.0,
            exit_threshold=0.0,
        )
    )

    data = pd.DataFrame(
        {
            "Close": [
                100,
                100,
                100,
                90,
            ]
        }
    )

    result = (
        strategy.generate_signals(
            data
        )
    )

    assert (
        result["Signal"]
        .iloc[-1]
        == 1
    )


def test_hold_and_exit_logic():

    strategy = (
        MeanReversionStrategy(
            lookback_period=3,
            entry_threshold=-1.0,
            exit_threshold=0.0,
        )
    )

    data = pd.DataFrame(
        {
            "Close": [
                100,
                100,
                100,
                90,
                92,
                100,
                110,
            ]
        }
    )

    result = (
        strategy.generate_signals(
            data
        )
    )

    assert (
        result["Signal"]
        .iloc[3]
        == 1
    )

    assert (
        result["Signal"]
        .iloc[-1]
        == 0
    )


def test_input_dataframe_not_modified():

    strategy = (
        MeanReversionStrategy(
            lookback_period=3
        )
    )

    original = pd.DataFrame(
        {
            "Close": [
                100,
                101,
                102,
                103,
            ]
        }
    )

    data = original.copy()

    strategy.generate_signals(
        data
    )

    pd.testing.assert_frame_equal(
        original,
        data,
    )