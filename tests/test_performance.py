import pandas as pd

from metrics.performance import (
    total_return,
    cagr,
    volatility,
    sharpe_ratio,
    sortino_ratio,
    max_drawdown,
    win_rate,
    profit_factor,
    number_of_trades,
    calculate_performance,
)


def make_equity_curve():

    return pd.DataFrame(
        {
            "Portfolio_Value": [
                100000,
                110000,
                120000,
            ],
            "Daily_Return": [
                0.0,
                0.10,
                0.090909,
            ],
        }
    )


def make_trade_history():

    return pd.DataFrame(
        {
            "Trade_PnL": [
                100,
                -50,
                200,
            ]
        }
    )


def test_total_return():

    equity = make_equity_curve()

    assert round(
        total_return(equity),
        2,
    ) == 0.20


def test_cagr_positive():

    equity = make_equity_curve()

    assert cagr(equity) > 0


def test_volatility_positive():

    equity = make_equity_curve()

    assert volatility(equity) > 0


def test_sharpe_ratio_returns_float():

    equity = make_equity_curve()

    result = sharpe_ratio(equity)

    assert isinstance(result, float)


def test_sortino_ratio_returns_float():

    equity = make_equity_curve()

    result = sortino_ratio(equity)

    assert isinstance(result, float)


def test_max_drawdown():

    equity = pd.DataFrame(
        {
            "Portfolio_Value": [
                100,
                120,
                90,
                130,
            ]
        }
    )

    assert round(
        max_drawdown(equity),
        2,
    ) == 0.25


def test_win_rate():

    trades = make_trade_history()

    assert round(
        win_rate(trades),
        2,
    ) == 0.67


def test_profit_factor():

    trades = make_trade_history()

    assert profit_factor(
        trades
    ) == 6.0


def test_number_of_trades():

    trades = make_trade_history()

    assert (
        number_of_trades(
            trades
        )
        == 3
    )


def test_calculate_performance():

    metrics = calculate_performance(
        make_equity_curve(),
        make_trade_history(),
    )

    assert "Total Return" in metrics
    assert "CAGR" in metrics
    assert "Volatility" in metrics
    assert "Sharpe Ratio" in metrics
    assert "Sortino Ratio" in metrics
    assert "Max Drawdown" in metrics
    assert "Win Rate" in metrics
    assert "Profit Factor" in metrics
    assert "Number of Trades" in metrics


def test_empty_trade_history():

    trade_history = pd.DataFrame(
        columns=["Trade_PnL"]
    )

    metrics = calculate_performance(
        make_equity_curve(),
        trade_history,
    )

    assert metrics["Win Rate"] == 0.0
    assert metrics["Profit Factor"] == 0.0
    assert metrics["Number of Trades"] == 0


def test_empty_equity_curve():

    equity_curve = pd.DataFrame(
        columns=[
            "Portfolio_Value",
            "Daily_Return",
        ]
    )

    metrics = calculate_performance(
        equity_curve,
        make_trade_history(),
    )

    assert metrics["Total Return"] == 0.0
    assert metrics["CAGR"] == 0.0
    assert metrics["Volatility"] == 0.0


def test_zero_volatility_sharpe():

    equity_curve = pd.DataFrame(
        {
            "Portfolio_Value": [
                100,
                100,
                100,
                100,
            ],
            "Daily_Return": [
                0.0,
                0.0,
                0.0,
                0.0,
            ],
        }
    )

    assert (
        sharpe_ratio(
            equity_curve
        )
        == 0.0
    )


def test_zero_volatility_sortino():

    equity_curve = pd.DataFrame(
        {
            "Portfolio_Value": [
                100,
                110,
                120,
            ],
            "Daily_Return": [
                0.0,
                0.10,
                0.05,
            ],
        }
    )

    assert (
        sortino_ratio(
            equity_curve
        )
        == 0.0
    )


def test_profit_factor_no_losses():

    trades = pd.DataFrame(
        {
            "Trade_PnL": [
                100,
                200,
                300,
            ]
        }
    )

    assert (
        profit_factor(trades)
        == float("inf")
    )


def test_profit_factor_no_trades():

    trades = pd.DataFrame(
        columns=["Trade_PnL"]
    )

    assert (
        profit_factor(
            trades
        )
        == 0.0
    )


def test_cagr_one_year():

    portfolio_values = [100000]

    daily_growth = (
        120000 / 100000
    ) ** (1 / 251)

    for _ in range(251):
        portfolio_values.append(
            portfolio_values[-1]
            * daily_growth
        )

    equity_curve = pd.DataFrame(
        {
            "Portfolio_Value":
                portfolio_values,
            "Daily_Return":
                [0.0] * 252,
        }
    )

    result = cagr(
        equity_curve
    )

    assert round(
        result,
        2,
    ) == 0.20



def test_profit_factor_infinite():

    trades = pd.DataFrame(
        {
            "Trade_PnL": [100, 200, 300]
        }
    )

    assert (
        profit_factor(trades)
        == float("inf")
    )


def test_single_row_cagr():

    equity = pd.DataFrame(
        {
            "Portfolio_Value": [100000],
            "Daily_Return": [0.0],
        }
    )

    assert cagr(equity) == 0.0


def test_single_row_volatility():

    equity = pd.DataFrame(
        {
            "Portfolio_Value": [100000],
            "Daily_Return": [0.0],
        }
    )

    assert volatility(equity) == 0.0


def test_single_row_sharpe():

    equity = pd.DataFrame(
        {
            "Portfolio_Value": [100000],
            "Daily_Return": [0.0],
        }
    )

    assert sharpe_ratio(equity) == 0.0


def test_single_row_sortino():

    equity = pd.DataFrame(
        {
            "Portfolio_Value": [100000],
            "Daily_Return": [0.0],
        }
    )

    assert sortino_ratio(equity) == 0.0


def test_sortino_single_downside_return():

    equity_curve = pd.DataFrame(
        {
            "Portfolio_Value": [
                100,
                99,
                105,
            ],
            "Daily_Return": [
                0.0,
                -0.01,
                0.06,
            ],
        }
    )

    assert sortino_ratio(equity_curve) == 0.0


def test_sortino_ratio_calculates():

    equity_curve = pd.DataFrame(
        {
            "Portfolio_Value": [
                100,
                95,
                90,
                100,
                110,
            ],
            "Daily_Return": [
                0.0,
                -0.05,
                -0.03,
                0.11,
                0.10,
            ],
        }
    )

    result = sortino_ratio(equity_curve)

    assert isinstance(result, float)
    assert result != 0.0


def test_profit_factor_zero_pnl():

    trades = pd.DataFrame(
        {
            "Trade_PnL": [
                0,
                0,
                0,
            ]
        }
    )

    assert profit_factor(trades) == 0.0


def test_sortino_zero_downside_std():

    equity_curve = pd.DataFrame(
        {
            "Portfolio_Value": [
                100,
                95,
                90,
                110,
            ],
            "Daily_Return": [
                0.0,
                -0.05,
                -0.05,
                0.22,
            ],
        }
    )

    assert (
        sortino_ratio(
            equity_curve
        )
        == 0.0
    )
