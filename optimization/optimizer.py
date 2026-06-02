from typing import Any
from typing import Dict
from typing import List
from typing import Type

import pandas as pd

from metrics.performance import (
    calculate_performance,
)


def optimize_strategy(
    data: pd.DataFrame,
    strategy_class: Type,
    parameter_grid: List[Dict[str, Any]],
    backtester,
    metric: str = "Sharpe Ratio",
) -> Dict[str, Any]:
    """
    Generic parameter optimization engine.
    """

    if not parameter_grid:

        return {
            "results": pd.DataFrame(),
            "best_parameters": {},
            "best_score": None,
            "best_metrics": {},
        }

    results = []

    for params in parameter_grid:

        try:

            if (
                "short_window" in params
                and "long_window" in params
                and params["short_window"]
                >= params["long_window"]
            ):
                continue

            if (
                "fast_window" in params
                and "slow_window" in params
                and params["fast_window"]
                >= params["slow_window"]
            ):
                continue

            strategy = strategy_class(
                **params
            )

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
                **params,
                **metrics,
            }

            results.append(row)

        except Exception as exc:

            print(
                f"Skipping parameters "
                f"{params}: {exc}"
            )

            continue

    results_df = pd.DataFrame(
        results
    )

    if results_df.empty:

        return {
            "results": results_df,
            "best_parameters": {},
            "best_score": None,
            "best_metrics": {},
        }

    if metric not in results_df.columns:
        raise ValueError(
            f"Metric '{metric}' "
            f"not found."
        )

    results_df = (
        results_df.sort_values(
            by=metric,
            ascending=False,
        )
        .reset_index(
            drop=True
        )
    )

    results_df.insert(
        0,
        "Rank",
        range(
            1,
            len(results_df) + 1,
        ),
    )

    best_row = results_df.iloc[0]

    parameter_keys = (
        parameter_grid[0].keys()
    )

    best_parameters = {}

    for key in parameter_keys:

        value = best_row[key]

        if hasattr(value, "item"):
            value = value.item()

        best_parameters[key] = value

    metric_columns = [
        column
        for column in results_df.columns
        if column
        not in (
            "Rank",
            *parameter_keys,
        )
    ]

    best_metrics = {
        column: best_row[column]
        for column in metric_columns
    }

    return {
        "results": results_df,
        "best_parameters":
            best_parameters,
        "best_score":
            best_row[metric],
        "best_metrics":
            best_metrics,
    }