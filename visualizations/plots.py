from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


def _create_output_dir(
    output_dir: str,
) -> Path:

    path = Path(output_dir)

    path.mkdir(
        parents=True,
        exist_ok=True,
    )

    return path


def _build_filename(
    strategy_name: str,
    chart_type: str,
    ticker: str | None = None,
) -> str:

    if ticker:
        return (
            f"{ticker}_"
            f"{strategy_name}_"
            f"{chart_type}.png"
        )

    return (
        f"{strategy_name}_"
        f"{chart_type}.png"
    )


def _save_or_show(
    path: Path,
    show: bool,
) -> None:

    plt.tight_layout()

    plt.savefig(path)

    if show:
        plt.show()

    plt.close()


def plot_signals(
    signal_df: pd.DataFrame,
    strategy_name: str,
    ticker: str | None = None,
    output_dir: str = "outputs/charts",
    show: bool = False,
) -> Path:

    required = {"Close", "Signal"}

    missing = required - set(
        signal_df.columns
    )

    if missing:
        raise ValueError(
            f"Missing columns: {missing}"
        )

    output_path = _create_output_dir(
        output_dir
    )

    filename = _build_filename(
        strategy_name,
        "signals",
        ticker,
    )

    full_path = output_path / filename

    signal_change = (
        signal_df["Signal"]
        .diff()
        .fillna(
            signal_df["Signal"]
        )
    )

    buy_signals = (
        signal_change == 1
    )

    sell_signals = (
        signal_change == -1
    )

    plt.figure(
        figsize=(12, 6)
    )

    plt.plot(
        signal_df.index,
        signal_df["Close"],
        label="Close",
    )

    if "SMA20" in signal_df.columns:
        plt.plot(
            signal_df.index,
            signal_df["SMA20"],
            label="SMA20",
        )

    if "SMA50" in signal_df.columns:
        plt.plot(
            signal_df.index,
            signal_df["SMA50"],
            label="SMA50",
        )

    plt.scatter(
        signal_df.index[
            buy_signals
        ],
        signal_df.loc[
            buy_signals,
            "Close",
        ],
        marker="^",
        s=100,
        label="Buy",
    )

    plt.scatter(
        signal_df.index[
            sell_signals
        ],
        signal_df.loc[
            sell_signals,
            "Close",
        ],
        marker="v",
        s=100,
        label="Sell",
    )

    plt.title(
        f"{strategy_name.upper()} "
        "Buy/Sell Signals"
    )

    plt.legend()

    _save_or_show(
        full_path,
        show,
    )

    return full_path


def plot_equity_curve(
    equity_curve: pd.DataFrame,
    strategy_name: str,
    ticker: str | None = None,
    output_dir: str = "outputs/charts",
    show: bool = False,
) -> Path:

    if (
        "Portfolio_Value"
        not in equity_curve.columns
    ):
        raise ValueError(
            "Portfolio_Value column missing"
        )

    output_path = _create_output_dir(
        output_dir
    )

    filename = _build_filename(
        strategy_name,
        "equity_curve",
        ticker,
    )

    full_path = output_path / filename

    initial_capital = (
        equity_curve[
            "Portfolio_Value"
        ].iloc[0]
    )

    plt.figure(
        figsize=(12, 6)
    )

    plt.plot(
        equity_curve.index,
        equity_curve[
            "Portfolio_Value"
        ],
        label="Portfolio Value",
    )

    plt.axhline(
        initial_capital,
        linestyle="--",
        label="Initial Capital",
    )

    plt.title(
        f"{strategy_name.upper()} "
        "Equity Curve"
    )

    plt.legend()

    _save_or_show(
        full_path,
        show,
    )

    return full_path


def plot_drawdown(
    equity_curve: pd.DataFrame,
    strategy_name: str,
    ticker: str | None = None,
    output_dir: str = "outputs/charts",
    show: bool = False,
) -> Path:

    if (
        "Portfolio_Value"
        not in equity_curve.columns
    ):
        raise ValueError(
            "Portfolio_Value column missing"
        )

    output_path = _create_output_dir(
        output_dir
    )

    filename = _build_filename(
        strategy_name,
        "drawdown",
        ticker,
    )

    full_path = output_path / filename

    portfolio = equity_curve[
        "Portfolio_Value"
    ]

    running_max = (
        portfolio.cummax()
    )

    drawdown = (
        portfolio
        / running_max
        - 1
    ) * 100

    plt.figure(
        figsize=(12, 6)
    )

    plt.fill_between(
        equity_curve.index,
        drawdown,
        0,
        alpha=0.3,
    )

    plt.plot(
        equity_curve.index,
        drawdown,
        label="Drawdown %",
    )

    plt.title(
        f"{strategy_name.upper()} "
        "Drawdown"
    )

    plt.legend()

    _save_or_show(
        full_path,
        show,
    )

    return full_path


def generate_all_charts(
    signal_df: pd.DataFrame,
    equity_curve: pd.DataFrame,
    strategy_name: str,
    ticker: str | None = None,
    output_dir: str = "outputs/charts",
    show: bool = False,
):

    return {
        "signals": plot_signals(
            signal_df,
            strategy_name,
            ticker,
            output_dir,
            show,
        ),
        "equity_curve": plot_equity_curve(
            equity_curve,
            strategy_name,
            ticker,
            output_dir,
            show,
        ),
        "drawdown": plot_drawdown(
            equity_curve,
            strategy_name,
            ticker,
            output_dir,
            show,
        ),
    }