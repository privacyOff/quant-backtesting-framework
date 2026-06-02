# import logging
# from pprint import pprint

# from backtester import Backtester
# from config import settings
# from data.downloader import download_data
# from metrics.performance import calculate_performance
# from reports.comparison import compare_strategies
# from strategies.mean_reversion import (
#     MeanReversionStrategy,
# )
# from strategies.momentum import (
#     MomentumStrategy,
# )
# from strategies.sma_crossover import (
#     SMACrossoverStrategy,
# )
# from visualizations.plots import (
#     generate_all_charts,
# )
# from optimization.optimizer import (
#     optimize_strategy,
# )


# logging.basicConfig(
#     level=logging.INFO,
#     format="%(levelname)s - %(message)s",
# )


# def run_strategy(
#     strategy,
#     data,
#     backtester,
#     ticker,
# ):
#     """
#     Run a single strategy end-to-end.
#     """

#     print(
#         f"\nRunning strategy: "
#         f"{strategy.name}"
#     )

#     signals = strategy.generate_signals(
#         data
#     )

#     results = backtester.run(
#         signals
#     )

#     metrics = calculate_performance(
#         results["equity_curve"],
#         results["trade_history"],
#     )

#     chart_paths = (
#         generate_all_charts(
#             signal_df=signals,
#             equity_curve=results[
#                 "equity_curve"
#             ],
#             strategy_name=(
#                 strategy.name
#             ),
#             ticker=ticker,
#         )
#     )

#     print(
#         "\nPerformance Metrics:"
#     )

#     pprint(metrics)

#     print(
#         "\nLast 5 Trades:"
#     )

#     print(
#         results[
#             "trade_history"
#         ].tail()
#     )

#     print(
#         "\nChart Files:"
#     )

#     pprint(chart_paths)

#     portfolio = results[
#         "equity_curve"
#     ]["Portfolio_Value"]

#     print(
#         "\nSanity Checks:"
#     )

#     print(
#         "Contains NaN:",
#         portfolio.isna().any(),
#     )

#     print(
#         "Negative Values:",
#         (portfolio < 0).any(),
#     )

#     print(
#         "Final Portfolio Value:",
#         portfolio.iloc[-1],
#     )

#     return {
#         "signals": signals,
#         "results": results,
#         "metrics": metrics,
#         "charts": chart_paths,
#     }


# def main():

#     print(
#         "\nDownloading data..."
#     )

#     market_data = download_data(
#         settings.tickers,
#         settings.start_date,
#         settings.end_date,
#     )

#     if not market_data:

#         print(
#             "No data downloaded."
#         )

#         return

#     ticker = None
#     data = None

#     for symbol, df in (
#         market_data.items()
#     ):

#         if not df.empty:

#             ticker = symbol
#             data = df

#             break

#     if data is None:

#         print(
#             "No valid market data."
#         )

#         return

#     print(
#         f"\nUsing ticker: "
#         f"{ticker}"
#     )

#     backtester = Backtester(
#         initial_capital=100000,
#         transaction_cost=0.001,
#         position_size=1.0,
#     )

#     strategies = [
#         SMACrossoverStrategy(),
#         MomentumStrategy(),
#         MeanReversionStrategy(),
#     ]

#     all_results = {}

#     print(
#         "\n"
#         + "=" * 80
#     )

#     print(
#         "INDIVIDUAL STRATEGY RUNS"
#     )

#     print(
#         "=" * 80
#     )

#     for strategy in strategies:

#         strategy_output = (
#             run_strategy(
#                 strategy=strategy,
#                 data=data,
#                 backtester=backtester,
#                 ticker=ticker,
#             )
#         )

#         all_results[
#             strategy.name
#         ] = strategy_output

#     print(
#         "\n"
#         + "=" * 80
#     )

#     print(
#         "STRATEGY COMPARISON"
#     )

#     print(
#         "=" * 80
#     )

#     comparison_df = (
#         compare_strategies(
#             data=data,
#             strategies=strategies,
#             backtester=backtester,
#         )
#     )

#     print(
#         comparison_df.to_string(
#             index=False
#         )
#     )

#     if not comparison_df.empty:

#         winner = (
#             comparison_df.iloc[0]
#         )

#         print(
#             "\n"
#             + "=" * 80
#         )

#         print(
#             "TOP STRATEGY"
#         )

#         print(
#             "=" * 80
#         )

#         print(
#             f"Rank: "
#             f"{winner['Rank']}"
#         )

#         print(
#             f"Strategy: "
#             f"{winner['Strategy']}"
#         )

#         print(
#             f"Sharpe Ratio: "
#             f"{winner['Sharpe Ratio']:.4f}"
#         )

#         print(
#             f"Total Return: "
#             f"{winner['Total Return']:.4%}"
#         )

#         print(
#             f"Max Drawdown: "
#             f"{winner['Max Drawdown']:.4%}"
#         )

#     print(
#         "\n"
#         + "=" * 80
#     )

#     print(
#         "COMPLETE"
#     )

#     print(
#         "=" * 80
#     )


# if __name__ == "__main__":
#     main()









import logging
from pprint import pprint

from backtester import Backtester
from config import settings
from data.downloader import download_data
from metrics.performance import calculate_performance
from reports.comparison import compare_strategies
from strategies.mean_reversion import (
    MeanReversionStrategy,
)
from strategies.momentum import (
    MomentumStrategy,
)
from strategies.sma_crossover import (
    SMACrossoverStrategy,
)
from visualizations.plots import (
    generate_all_charts,
)
from optimization.optimizer import (
    optimize_strategy,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
)


def run_strategy(
    strategy,
    data,
    backtester,
    ticker,
):
    """
    Run a single strategy end-to-end.
    """

    print(
        f"\nRunning strategy: "
        f"{strategy.name}"
    )

    signals = strategy.generate_signals(
        data
    )

    results = backtester.run(
        signals
    )

    metrics = calculate_performance(
        results["equity_curve"],
        results["trade_history"],
    )

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

    print(
        "\nPerformance Metrics:"
    )

    pprint(metrics)

    print(
        "\nLast 5 Trades:"
    )

    print(
        results[
            "trade_history"
        ].tail()
    )

    print(
        "\nChart Files:"
    )

    pprint(chart_paths)

    portfolio = results[
        "equity_curve"
    ]["Portfolio_Value"]

    print(
        "\nSanity Checks:"
    )

    print(
        "Contains NaN:",
        portfolio.isna().any(),
    )

    print(
        "Negative Values:",
        (portfolio < 0).any(),
    )

    print(
        "Final Portfolio Value:",
        portfolio.iloc[-1],
    )

    return {
        "signals": signals,
        "results": results,
        "metrics": metrics,
        "charts": chart_paths,
    }


def main():

    print(
        "\nDownloading data..."
    )

    market_data = download_data(
        settings.tickers,
        settings.start_date,
        settings.end_date,
    )

    if not market_data:

        print(
            "No data downloaded."
        )

        return

    ticker = None
    data = None

    for symbol, df in (
        market_data.items()
    ):

        if not df.empty:

            ticker = symbol
            data = df

            break

    if data is None:

        print(
            "No valid market data."
        )

        return

    print(
        f"\nUsing ticker: "
        f"{ticker}"
    )

    backtester = Backtester(
        initial_capital=100000,
        transaction_cost=0.001,
        position_size=1.0,
    )

    strategies = [
        SMACrossoverStrategy(),
        MomentumStrategy(),
        MeanReversionStrategy(),
    ]

    all_results = {}

    print(
        "\n"
        + "=" * 80
    )

    print(
        "INDIVIDUAL STRATEGY RUNS"
    )

    print(
        "=" * 80
    )

    for strategy in strategies:

        strategy_output = (
            run_strategy(
                strategy=strategy,
                data=data,
                backtester=backtester,
                ticker=ticker,
            )
        )

        all_results[
            strategy.name
        ] = strategy_output

    print(
        "\n"
        + "=" * 80
    )

    print(
        "STRATEGY COMPARISON"
    )

    print(
        "=" * 80
    )

    comparison_df = (
        compare_strategies(
            data=data,
            strategies=strategies,
            backtester=backtester,
        )
    )

    print(
        comparison_df.to_string(
            index=False
        )
    )

    if not comparison_df.empty:

        winner = (
            comparison_df.iloc[0]
        )

        print(
            "\n"
            + "=" * 80
        )

        print(
            "TOP STRATEGY"
        )

        print(
            "=" * 80
        )

        print(
            f"Rank: "
            f"{winner['Rank']}"
        )

        print(
            f"Strategy: "
            f"{winner['Strategy']}"
        )

        print(
            f"Sharpe Ratio: "
            f"{winner['Sharpe Ratio']:.4f}"
        )

        print(
            f"Total Return: "
            f"{winner['Total Return']:.4%}"
        )

        print(
            f"Max Drawdown: "
            f"{winner['Max Drawdown']:.4%}"
        )

    print(
        "\n"
        + "=" * 80
    )

    print(
        "SMA OPTIMIZATION"
    )

    print(
        "=" * 80
    )

    optimization = optimize_strategy(
        data=data,
        strategy_class=SMACrossoverStrategy,
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
        backtester=backtester,
    )

    print(
        optimization[
            "results"
        ].to_string(
            index=False
        )
    )

    print(
        "\nBest Parameters:"
    )

    print(
        optimization[
            "best_parameters"
        ]
    )

    print(
        "\nBest Sharpe:"
    )

    print(
        optimization[
            "best_score"
        ]
    )

    print(
        "\n"
        + "=" * 80
    )

    print(
        "COMPLETE"
    )

    print(
        "=" * 80
    )


if __name__ == "__main__":
    main()