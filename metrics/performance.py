# from typing import Dict

# import numpy as np
# import pandas as pd


# TRADING_DAYS = 252


# def total_return(equity_curve: pd.DataFrame) -> float:
#     portfolio = equity_curve["Portfolio_Value"]

#     if portfolio.empty:
#         return 0.0

#     return (
#         portfolio.iloc[-1]
#         / portfolio.iloc[0]
#         - 1
#     )


# def cagr(equity_curve: pd.DataFrame) -> float:
#     portfolio = equity_curve["Portfolio_Value"]

#     if portfolio.empty:
#         return 0.0

#     years = len(portfolio) / TRADING_DAYS

#     if years <= 0:
#         return 0.0

#     return (
#         portfolio.iloc[-1]
#         / portfolio.iloc[0]
#     ) ** (1 / years) - 1


# def volatility(equity_curve: pd.DataFrame) -> float:
#     returns = equity_curve["Daily_Return"]

#     if returns.empty:
#         return 0.0

#     return (
#         returns.std()
#         * np.sqrt(TRADING_DAYS)
#     )


# def sharpe_ratio(
#     equity_curve: pd.DataFrame,
#     risk_free_rate: float = 0.0,
# ) -> float:
#     returns = equity_curve["Daily_Return"]

#     if returns.empty:
#         return 0.0

#     volatility_daily = returns.std()

#     if volatility_daily == 0:
#         return 0.0

#     excess_return = (
#         returns.mean()
#         - risk_free_rate / TRADING_DAYS
#     )

#     return (
#         excess_return
#         / volatility_daily
#         * np.sqrt(TRADING_DAYS)
#     )


# def sortino_ratio(
#     equity_curve: pd.DataFrame,
#     risk_free_rate: float = 0.0,
# ) -> float:
#     returns = equity_curve["Daily_Return"]

#     if returns.empty:
#         return 0.0

#     downside_returns = returns[
#         returns < 0
#     ]

#     downside_std = downside_returns.std()

#     if (
#         downside_returns.empty
#         or downside_std == 0
#     ):
#         return 0.0

#     excess_return = (
#         returns.mean()
#         - risk_free_rate / TRADING_DAYS
#     )

#     return (
#         excess_return
#         / downside_std
#         * np.sqrt(TRADING_DAYS)
#     )


# def max_drawdown(
#     equity_curve: pd.DataFrame,
# ) -> float:
#     portfolio = equity_curve["Portfolio_Value"]

#     if portfolio.empty:
#         return 0.0

#     running_max = portfolio.cummax()

#     drawdown = (
#         portfolio
#         / running_max
#         - 1
#     )

#     return abs(drawdown.min())


# def win_rate(
#     trade_history: pd.DataFrame,
# ) -> float:
#     if trade_history.empty:
#         return 0.0

#     winners = (
#         trade_history["Trade_PnL"] > 0
#     ).sum()

#     return winners / len(trade_history)


# def profit_factor(
#     trade_history: pd.DataFrame,
# ) -> float:
#     if trade_history.empty:
#         return 0.0

#     profits = trade_history.loc[
#         trade_history["Trade_PnL"] > 0,
#         "Trade_PnL",
#     ].sum()

#     losses = abs(
#         trade_history.loc[
#             trade_history["Trade_PnL"] < 0,
#             "Trade_PnL",
#         ].sum()
#     )

#     if losses == 0:
#         return 0.0

#     return profits / losses


# def number_of_trades(
#     trade_history: pd.DataFrame,
# ) -> int:
#     return len(trade_history)


# def calculate_performance(
#     equity_curve: pd.DataFrame,
#     trade_history: pd.DataFrame,
#     risk_free_rate: float = 0.0,
# ) -> Dict[str, float]:

#     return {
#         "Total Return":
#             total_return(equity_curve),

#         "CAGR":
#             cagr(equity_curve),

#         "Volatility":
#             volatility(equity_curve),

#         "Sharpe Ratio":
#             sharpe_ratio(
#                 equity_curve,
#                 risk_free_rate,
#             ),

#         "Sortino Ratio":
#             sortino_ratio(
#                 equity_curve,
#                 risk_free_rate,
#             ),

#         "Max Drawdown":
#             max_drawdown(
#                 equity_curve
#             ),

#         "Win Rate":
#             win_rate(
#                 trade_history
#             ),

#         "Profit Factor":
#             profit_factor(
#                 trade_history
#             ),

#         "Number of Trades":
#             number_of_trades(
#                 trade_history
#             ),
#     }





from typing import Dict

import numpy as np
import pandas as pd


TRADING_DAYS = 252


def total_return(equity_curve: pd.DataFrame) -> float:
    """
    Total portfolio return.
    """
    portfolio = equity_curve["Portfolio_Value"]

    if portfolio.empty:
        return 0.0

    return (
        portfolio.iloc[-1]
        / portfolio.iloc[0]
        - 1
    )


def cagr(equity_curve: pd.DataFrame) -> float:
    """
    Compound Annual Growth Rate.
    """
    portfolio = equity_curve["Portfolio_Value"]

    if len(portfolio) < 2:
        return 0.0

    years = (len(portfolio) - 1) / TRADING_DAYS

    return (
        portfolio.iloc[-1]
        / portfolio.iloc[0]
    ) ** (1 / years) - 1


def volatility(equity_curve: pd.DataFrame) -> float:
    """
    Annualized volatility.
    """
    returns = equity_curve["Daily_Return"]

    if len(returns) < 2:
        return 0.0

    return (
        returns.std(ddof=1)
        * np.sqrt(TRADING_DAYS)
    )


def sharpe_ratio(
    equity_curve: pd.DataFrame,
    risk_free_rate: float = 0.0,
) -> float:
    """
    Annualized Sharpe Ratio.
    """
    returns = equity_curve["Daily_Return"]

    if len(returns) < 2:
        return 0.0

    volatility_daily = returns.std(ddof=1)

    if volatility_daily == 0 or np.isnan(volatility_daily):
        return 0.0

    excess_return = (
        returns.mean()
        - risk_free_rate / TRADING_DAYS
    )

    return (
        excess_return
        / volatility_daily
        * np.sqrt(TRADING_DAYS)
    )


def sortino_ratio(
    equity_curve: pd.DataFrame,
    risk_free_rate: float = 0.0,
) -> float:
    """
    Annualized Sortino Ratio.
    """
    returns = equity_curve["Daily_Return"]

    if len(returns) < 2:
        return 0.0

    downside_returns = returns[
        returns < 0
    ]

    if len(downside_returns) < 2:
        return 0.0

    downside_std = downside_returns.std(
        ddof=1
    )

    if downside_std == 0 or np.isnan(
        downside_std
    ):
        return 0.0

    excess_return = (
        returns.mean()
        - risk_free_rate / TRADING_DAYS
    )

    return (
        excess_return
        / downside_std
        * np.sqrt(TRADING_DAYS)
    )


def max_drawdown(
    equity_curve: pd.DataFrame,
) -> float:
    """
    Maximum drawdown returned as
    a positive percentage.

    Example:
        0.25 = 25% drawdown
    """
    portfolio = equity_curve["Portfolio_Value"]

    if portfolio.empty:
        return 0.0

    running_max = portfolio.cummax()

    drawdown = (
        portfolio
        / running_max
        - 1
    )

    return abs(drawdown.min())


def win_rate(
    trade_history: pd.DataFrame,
) -> float:
    """
    Percentage of winning trades.
    """
    if trade_history.empty:
        return 0.0

    winners = (
        trade_history["Trade_PnL"] > 0
    ).sum()

    return winners / len(trade_history)


def profit_factor(
    trade_history: pd.DataFrame,
) -> float:
    """
    Gross profits divided by
    gross losses.
    """
    if trade_history.empty:
        return 0.0

    profits = trade_history.loc[
        trade_history["Trade_PnL"] > 0,
        "Trade_PnL",
    ].sum()

    losses = abs(
        trade_history.loc[
            trade_history["Trade_PnL"] < 0,
            "Trade_PnL",
        ].sum()
    )

    if losses == 0:

        if profits > 0:
            return float("inf")

        return 0.0

    return profits / losses


def number_of_trades(
    trade_history: pd.DataFrame,
) -> int:
    """
    Total completed trades.
    """
    return len(trade_history)


def calculate_performance(
    equity_curve: pd.DataFrame,
    trade_history: pd.DataFrame,
    risk_free_rate: float = 0.0,
) -> Dict[str, float]:
    """
    Calculate all performance metrics.
    """

    return {
        "Total Return":
            total_return(
                equity_curve
            ),

        "CAGR":
            cagr(
                equity_curve
            ),

        "Volatility":
            volatility(
                equity_curve
            ),

        "Sharpe Ratio":
            sharpe_ratio(
                equity_curve,
                risk_free_rate,
            ),

        "Sortino Ratio":
            sortino_ratio(
                equity_curve,
                risk_free_rate,
            ),

        "Max Drawdown":
            max_drawdown(
                equity_curve
            ),

        "Win Rate":
            win_rate(
                trade_history
            ),

        "Profit Factor":
            profit_factor(
                trade_history
            ),

        "Number of Trades":
            number_of_trades(
                trade_history
            ),
    }