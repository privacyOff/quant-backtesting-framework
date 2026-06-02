import pandas as pd

from backtester import Backtester

from optimization.optimizer import (
    optimize_strategy,
)

from strategies.base_strategy import (
    BaseStrategy,
)

from strategies.sma_crossover import (
    SMACrossoverStrategy,
)


def sample_data():

    prices = []

    for i in range(400):

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


def test_returns_dictionary():

    result = optimize_strategy(
        data=sample_data(),
        strategy_class=(
            SMACrossoverStrategy
        ),
        parameter_grid=[
            {
                "fast_window": 10,
                "slow_window": 30,
            }
        ],
        backtester=(
            make_backtester()
        ),
    )

    assert (
        "results" in result
    )

    assert (
        "best_parameters"
        in result
    )

    assert (
        "best_score"
        in result
    )

    assert (
        "best_metrics"
        in result
    )


def test_results_is_dataframe():

    result = optimize_strategy(
        data=sample_data(),
        strategy_class=(
            SMACrossoverStrategy
        ),
        parameter_grid=[
            {
                "fast_window": 10,
                "slow_window": 30,
            }
        ],
        backtester=(
            make_backtester()
        ),
    )

    assert isinstance(
        result["results"],
        pd.DataFrame,
    )


def test_rank_column_exists():

    result = optimize_strategy(
        data=sample_data(),
        strategy_class=(
            SMACrossoverStrategy
        ),
        parameter_grid=[
            {
                "fast_window": 10,
                "slow_window": 30,
            },
            {
                "fast_window": 20,
                "slow_window": 50,
            },
        ],
        backtester=(
            make_backtester()
        ),
    )

    assert (
        "Rank"
        in result[
            "results"
        ].columns
    )


def test_rank_values():

    result = optimize_strategy(
        data=sample_data(),
        strategy_class=(
            SMACrossoverStrategy
        ),
        parameter_grid=[
            {
                "fast_window": 10,
                "slow_window": 30,
            },
            {
                "fast_window": 20,
                "slow_window": 50,
            },
        ],
        backtester=(
            make_backtester()
        ),
    )

    ranks = result[
        "results"
    ]["Rank"].tolist()

    assert ranks == [1, 2]


def test_sorted_by_sharpe():

    result = optimize_strategy(
        data=sample_data(),
        strategy_class=(
            SMACrossoverStrategy
        ),
        parameter_grid=[
            {
                "fast_window": 10,
                "slow_window": 30,
            },
            {
                "fast_window": 20,
                "slow_window": 50,
            },
            {
                "fast_window": 50,
                "slow_window": 200,
            },
        ],
        backtester=(
            make_backtester()
        ),
    )

    sharpe = result[
        "results"
    ][
        "Sharpe Ratio"
    ].tolist()

    assert sharpe == sorted(
        sharpe,
        reverse=True,
    )


def test_best_parameters_match_top_row():

    result = optimize_strategy(
        data=sample_data(),
        strategy_class=(
            SMACrossoverStrategy
        ),
        parameter_grid=[
            {
                "fast_window": 10,
                "slow_window": 30,
            },
            {
                "fast_window": 20,
                "slow_window": 50,
            },
        ],
        backtester=(
            make_backtester()
        ),
    )

    best_row = (
        result["results"]
        .iloc[0]
    )

    assert (
        result[
            "best_parameters"
        ][
            "fast_window"
        ]
        == best_row[
            "fast_window"
        ]
    )


def test_empty_grid():

    result = optimize_strategy(
        data=sample_data(),
        strategy_class=(
            SMACrossoverStrategy
        ),
        parameter_grid=[],
        backtester=(
            make_backtester()
        ),
    )

    assert result[
        "results"
    ].empty

    assert (
        result[
            "best_parameters"
        ]
        == {}
    )


def test_invalid_sma_parameters_skipped():

    result = optimize_strategy(
        data=sample_data(),
        strategy_class=(
            SMACrossoverStrategy
        ),
        parameter_grid=[
            {
                "fast_window": 50,
                "slow_window": 20,
            },
            {
                "fast_window": 10,
                "slow_window": 30,
            },
        ],
        backtester=(
            make_backtester()
        ),
    )

    assert (
        len(
            result["results"]
        )
        == 1
    )


class BrokenStrategy(
    BaseStrategy
):

    def __init__(
        self,
        **kwargs,
    ):
        pass

    def generate_signals(
        self,
        data,
    ):
        raise RuntimeError(
            "Broken strategy"
        )


def test_broken_strategy_skipped():

    result = optimize_strategy(
        data=sample_data(),
        strategy_class=(
            BrokenStrategy
        ),
        parameter_grid=[
            {
                "x": 1
            }
        ],
        backtester=(
            make_backtester()
        ),
    )

    assert result[
        "results"
    ].empty