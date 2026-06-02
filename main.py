import argparse

from cli.commands import (
    run_strategy,
    run_comparison,
    run_optimization,
    list_strategies,
    show_version,
)


def parse_args():

    parser = argparse.ArgumentParser(
        description=(
            "Quant Backtester CLI"
        )
    )

    parser.add_argument(
        "--strategy",
        default="sma",
        choices=[
            "sma",
            "momentum",
            "mean_reversion",
        ],
    )

    parser.add_argument(
        "--ticker",
        default="AAPL",
    )

    parser.add_argument(
        "--compare",
        action="store_true",
    )

    parser.add_argument(
        "--optimize",
        action="store_true",
    )

    parser.add_argument(
        "--list-strategies",
        action="store_true",
    )

    parser.add_argument(
        "--version",
        action="store_true",
    )

    return parser.parse_args()


def main():

    args = parse_args()

    if args.version:

        print(
            show_version()
        )
        return

    if args.list_strategies:

        for strategy in (
            list_strategies()
        ):
            print(strategy)

        return

    if args.compare:

        run_comparison(
            args.ticker
        )
        return

    if args.optimize:

        run_optimization(
            args.ticker
        )
        return

    run_strategy(
        ticker=args.ticker,
        strategy_name=(
            args.strategy
        ),
    )


if __name__ == "__main__":
    main()