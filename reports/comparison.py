from typing import List

import pandas as pd

from metrics.performance import (
    calculate_performance,
)


def compare_strategies(
    data: pd.DataFrame,
    strategies: List,
    backtester,
    sort_by: str = "Sharpe Ratio",
) -> pd.DataFrame:
    """
    Run multiple strategies against the same dataset.

    Parameters
    ----------
    data : pd.DataFrame

    strategies : list
        List of strategy objects.

    backtester : Backtester

    sort_by : str
        Metric used for ranking.

    Returns
    -------
    pd.DataFrame
    """

    if not strategies:
        return pd.DataFrame()

    results = []

    for strategy in strategies:

        try:

            signals = (
                strategy.generate_signals(
                    data
                )
            )

            backtest_results = (
                backtester.run(
                    signals
                )
            )

            metrics = (
                calculate_performance(
                    backtest_results[
                        "equity_curve"
                    ],
                    backtest_results[
                        "trade_history"
                    ],
                )
            )

            row = {
                "Strategy":
                    strategy.name,
                **metrics,
            }

            results.append(row)

        except Exception as exc:

            print(
                f"Strategy "
                f"{strategy.__class__.__name__} "
                f"failed: {exc}"
            )

            continue

    comparison_df = pd.DataFrame(
        results
    )

    if comparison_df.empty:
        return comparison_df

    if sort_by in comparison_df.columns:

        comparison_df = (
            comparison_df.sort_values(
                by=sort_by,
                ascending=False,
            )
            .reset_index(
                drop=True
            )
        )

    comparison_df.insert(
        0,
        "Rank",
        range(
            1,
            len(comparison_df) + 1,
        ),
    )

    return comparison_df