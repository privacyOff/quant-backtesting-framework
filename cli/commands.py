from pprint import pprint

from rich.console import Console
from rich.table import Table

from backtester import Backtester
from config import settings
from data.downloader import download_data

from metrics.performance import (
    calculate_performance,
)

from optimization.optimizer import (
    optimize_strategy,
)

from reports.comparison import (
    compare_strategies,
)

from strategies import (
    SMACrossoverStrategy,
    MomentumStrategy,
    MeanReversionStrategy,
)

from visualizations.plots import (
    generate_all_charts,
)

from .registry import STRATEGIES


console = Console()


VERSION = "Quant Backtester v1.0.0"


def show_version() -> str:
    return VERSION


def list_strategies():

    return list(
        STRATEGIES.keys()
    )


def display_metrics(metrics):

    table = Table(
        title="Performance Metrics"
    )

    table.add_column("Metric")
    table.add_column("Value")

    for key, value in metrics.items():

        table.add_row(
            str(key),
            str(value),
        )

    console.print(table)


def display_dataframe(
    df,
    title,
):

    table = Table(
        title=title
    )

    for column in df.columns:
        table.add_column(
            str(column)
        )

    for _, row in df.iterrows():

        table.add_row(
            *[
                str(v)
                for v in row.values
            ]
        )

    console.print(table)


def run_strategy(
    ticker: str,
    strategy_name: str,
):

    market_data = download_data(
        [ticker],
        settings.start_date,
        settings.end_date,
    )

    if ticker not in market_data:
        raise ValueError(
            f"Unable to load {ticker}"
        )

    strategy_class = STRATEGIES[
        strategy_name
    ]

    strategy = strategy_class()

    backtester = Backtester(
        initial_capital=settings.initial_capital,
    )

    signals = (
        strategy.generate_signals(
            market_data[ticker]
        )
    )

    results = backtester.run(
        signals
    )

    metrics = (
        calculate_performance(
            results["equity_curve"],
            results["trade_history"],
        )
    )

    display_metrics(metrics)

    chart_paths = (
        generate_all_charts(
            signal_df=signals,
            equity_curve=results[
                "equity_curve"
            ],
            strategy_name=(
                strategy.name
            ),
            ticker=ticker,
        )
    )

    console.print(
        "\nGenerated Charts:"
    )

    pprint(chart_paths)

    return {
        "signals": signals,
        "results": results,
        "metrics": metrics,
        "charts": chart_paths,
    }


def run_comparison(
    ticker: str,
):

    market_data = download_data(
        [ticker],
        settings.start_date,
        settings.end_date,
    )

    data = market_data[ticker]

    comparison = (
        compare_strategies(
            data=data,
            strategies=[
                SMACrossoverStrategy(),
                MomentumStrategy(),
                MeanReversionStrategy(),
            ],
            backtester=Backtester(
                initial_capital=settings.initial_capital,
            ),
        )
    )

    display_dataframe(
        comparison,
        "Strategy Comparison",
    )

    return comparison


def run_optimization(
    ticker: str,
):

    market_data = download_data(
        [ticker],
        settings.start_date,
        settings.end_date,
    )

    data = market_data[ticker]

    parameter_grid = [
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
    ]

    result = (
        optimize_strategy(
            data=data,
            strategy_class=(
                SMACrossoverStrategy
            ),
            parameter_grid=(
                parameter_grid
            ),
            backtester=Backtester(
                initial_capital=settings.initial_capital,
            ),
        )
    )

    display_dataframe(
        result["results"],
        "SMA Optimization",
    )

    console.print(
        "\nBest Parameters:"
    )

    pprint(
        result[
            "best_parameters"
        ]
    )

    return result