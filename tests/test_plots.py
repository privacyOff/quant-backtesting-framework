from pathlib import Path

import pandas as pd

from visualizations.plots import (
    plot_signals,
    plot_equity_curve,
    plot_drawdown,
    generate_all_charts,
)


def sample_signal_df():

    dates = pd.date_range(
        "2024-01-01",
        periods=10,
    )

    return pd.DataFrame(
        {
            "Close": [
                100,
                101,
                102,
                103,
                104,
                103,
                105,
                107,
                108,
                110,
            ],
            "Signal": [
                0,
                0,
                1,
                1,
                1,
                0,
                0,
                1,
                1,
                0,
            ],
            "SMA20": [
                100,
                100,
                101,
                102,
                103,
                103,
                104,
                105,
                106,
                107,
            ],
            "SMA50": [
                100,
                100,
                100,
                101,
                101,
                102,
                102,
                103,
                104,
                105,
            ],
        },
        index=dates,
    )


def sample_equity_curve():

    dates = pd.date_range(
        "2024-01-01",
        periods=10,
    )

    return pd.DataFrame(
        {
            "Portfolio_Value": [
                100000,
                101000,
                102500,
                101500,
                103000,
                105000,
                104000,
                106000,
                108000,
                110000,
            ]
        },
        index=dates,
    )


def test_plot_signals_creates_file(
    tmp_path,
):

    output = plot_signals(
        sample_signal_df(),
        strategy_name="sma",
        ticker="AAPL",
        output_dir=str(
            tmp_path
        ),
    )

    assert output.exists()


def test_plot_equity_curve_creates_file(
    tmp_path,
):

    output = plot_equity_curve(
        sample_equity_curve(),
        strategy_name="sma",
        ticker="AAPL",
        output_dir=str(
            tmp_path
        ),
    )

    assert output.exists()


def test_plot_drawdown_creates_file(
    tmp_path,
):

    output = plot_drawdown(
        sample_equity_curve(),
        strategy_name="sma",
        ticker="AAPL",
        output_dir=str(
            tmp_path
        ),
    )

    assert output.exists()


def test_generate_all_charts(
    tmp_path,
):

    result = generate_all_charts(
        signal_df=sample_signal_df(),
        equity_curve=sample_equity_curve(),
        strategy_name="sma",
        ticker="AAPL",
        output_dir=str(
            tmp_path
        ),
    )

    assert result[
        "signals"
    ].exists()

    assert result[
        "equity_curve"
    ].exists()

    assert result[
        "drawdown"
    ].exists()


def test_directory_created_automatically(
    tmp_path,
):

    nested = (
        tmp_path
        / "new"
        / "charts"
    )

    plot_signals(
        sample_signal_df(),
        strategy_name="sma",
        output_dir=str(
            nested
        ),
    )

    assert nested.exists()