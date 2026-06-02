from pprint import pprint

from backtester import Backtester
from config import settings
from data.downloader import download_data
from metrics.performance import (
    calculate_performance,
)
from strategies.sma_crossover import (
    SMACrossoverStrategy,
)
from visualizations.plots import (
    generate_all_charts,
)


def main():

    print("\nDownloading data...")

    market_data = download_data(
        settings.tickers,
        settings.start_date,
        settings.end_date,
    )

    ticker = settings.tickers[0]

    print(
        f"\nRunning strategy on: {ticker}"
    )

    strategy = SMACrossoverStrategy()

    signals = strategy.generate_signals(
        market_data[ticker]
    )

    backtester = Backtester(
        initial_capital=100000,
        transaction_cost=0.001,
        position_size=1.0,
    )

    results = backtester.run(signals)

    metrics = calculate_performance(
        results["equity_curve"],
        results["trade_history"],
    )

    print("\n" + "=" * 60)
    print("PERFORMANCE METRICS")
    print("=" * 60)

    pprint(metrics)

    print("\n" + "=" * 60)
    print("TRADE HISTORY")
    print("=" * 60)

    print(
        results["trade_history"].tail()
    )

    print("\n" + "=" * 60)
    print("EQUITY CURVE")
    print("=" * 60)

    print(
        results["equity_curve"][
            [
                "Portfolio_Value",
            ]
        ].tail()
    )

    chart_paths = generate_all_charts(
        signal_df=signals,
        equity_curve=results[
            "equity_curve"
        ],
        strategy_name="sma",
        ticker=ticker,
    )

    print("\n" + "=" * 60)
    print("GENERATED CHARTS")
    print("=" * 60)

    pprint(chart_paths)

    print("\n" + "=" * 60)
    print("SANITY CHECKS")
    print("=" * 60)

    portfolio = results[
        "equity_curve"
    ]["Portfolio_Value"]

    print(
        "Contains NaN:",
        portfolio.isna().any(),
    )

    print(
        "Any Negative Values:",
        (portfolio < 0).any(),
    )

    print(
        "Final Portfolio Value:",
        portfolio.iloc[-1],
    )

    if not results[
        "trade_history"
    ].empty:

        pnl_sum = results[
            "trade_history"
        ]["Trade_PnL"].sum()

        print(
            "Trade PnL Sum:",
            pnl_sum,
        )

        print(
            "Expected Final Value:",
            100000 + pnl_sum,
        )


if __name__ == "__main__":
    main()