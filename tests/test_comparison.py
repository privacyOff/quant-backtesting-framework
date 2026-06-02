import pandas as pd

from backtester import Backtester

from reports.comparison import (
    compare_strategies,
)

from strategies.base_strategy import (
    BaseStrategy,
)

from strategies.sma_crossover import (
    SMACrossoverStrategy,
)

from strategies.momentum import (
    MomentumStrategy,
)

from strategies.mean_reversion import (
    MeanReversionStrategy,
)


def sample_data():

    prices = []

    for i in range(300):
        prices.append(
            100 + i * 0.5
        )

    return pd.DataFrame(
        {
            "Close": prices
        }
    )


def make_backtester():

    return Backtester(
        initial_capital=100000,
        transaction_cost=0.001,
        position_size=1.0,
    )


def test_returns_dataframe():

    result = compare_strategies(
        data=sample_data(),
        strategies=[
            SMACrossoverStrategy(),
            MomentumStrategy(),
            MeanReversionStrategy(),
        ],
        backtester=make_backtester(),
    )

    assert isinstance(
        result,
        pd.DataFrame,
    )


def test_contains_strategies():

    result = compare_strategies(
        data=sample_data(),
        strategies=[
            SMACrossoverStrategy(),
            MomentumStrategy(),
            MeanReversionStrategy(),
        ],
        backtester=make_backtester(),
    )

    strategies = set(
        result["Strategy"]
    )

    assert "Momentum" in strategies
    assert "MeanReversion" in strategies


def test_expected_columns():

    result = compare_strategies(
        data=sample_data(),
        strategies=[
            SMACrossoverStrategy(),
            MomentumStrategy(),
            MeanReversionStrategy(),
        ],
        backtester=make_backtester(),
    )

    expected = {
        "Rank",
        "Strategy",
        "Total Return",
        "CAGR",
        "Volatility",
        "Sharpe Ratio",
        "Sortino Ratio",
        "Max Drawdown",
        "Win Rate",
        "Profit Factor",
        "Number of Trades",
    }

    assert expected.issubset(
        result.columns
    )


def test_rank_column():

    result = compare_strategies(
        data=sample_data(),
        strategies=[
            SMACrossoverStrategy(),
            MomentumStrategy(),
            MeanReversionStrategy(),
        ],
        backtester=make_backtester(),
    )

    expected = list(
        range(
            1,
            len(result) + 1,
        )
    )

    assert (
        result["Rank"]
        .tolist()
        == expected
    )


def test_sorted_by_sharpe():

    result = compare_strategies(
        data=sample_data(),
        strategies=[
            SMACrossoverStrategy(),
            MomentumStrategy(),
            MeanReversionStrategy(),
        ],
        backtester=make_backtester(),
    )

    sharpe = result[
        "Sharpe Ratio"
    ].tolist()

    assert sharpe == sorted(
        sharpe,
        reverse=True,
    )


def test_empty_strategy_list():

    result = compare_strategies(
        data=sample_data(),
        strategies=[],
        backtester=make_backtester(),
    )

    assert result.empty


class BrokenStrategy(
    BaseStrategy
):

    def __init__(self):

        self.name = "Broken"

        self.parameters = {}

    def generate_signals(
        self,
        data,
    ):

        raise RuntimeError(
            "Intentional failure"
        )


def test_broken_strategy_does_not_stop_comparison():

    result = compare_strategies(
        data=sample_data(),
        strategies=[
            SMACrossoverStrategy(),
            BrokenStrategy(),
            MomentumStrategy(),
        ],
        backtester=make_backtester(),
    )

    assert not result.empty

    assert (
        "Broken"
        not in result[
            "Strategy"
        ].values
    )