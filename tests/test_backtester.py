import pandas as pd
import pytest

from backtester import Backtester


def sample_df():
    dates = pd.date_range("2024-01-01", periods=6, freq="D")
    return pd.DataFrame(
        {
            "Close": [100, 100, 110, 120, 115, 130],
            "Signal": [0, 1, 1, 0, 0, 0],
        },
        index=dates,
    )


def test_constructor_validation():
    with pytest.raises(ValueError):
        Backtester(0)

    with pytest.raises(ValueError):
        Backtester(1000, transaction_cost=-0.1)

    with pytest.raises(ValueError):
        Backtester(1000, position_size=0)


def test_missing_columns():
    bt = Backtester(1000)
    with pytest.raises(ValueError):
        bt.run(pd.DataFrame({"Close": [1, 2, 3]}))


def test_position_generation():
    bt = Backtester(1000)
    result = bt.run(sample_df())

    positions = result["equity_curve"]["Position"].tolist()
    assert positions == [0, 0, 1, 1, 0, 0]


def test_equity_curve_starts_with_capital():
    bt = Backtester(1000)
    result = bt.run(sample_df())

    assert result["equity_curve"]["Portfolio_Value"].iloc[0] == 1000


def test_daily_returns_exist():
    bt = Backtester(1000)
    result = bt.run(sample_df())

    assert "Daily_Return" in result["equity_curve"].columns


def test_trade_detection():
    bt = Backtester(1000)
    result = bt.run(sample_df())

    trades = result["trade_history"]
    assert len(trades) == 1


def test_transaction_costs_reduce_pnl():
    no_cost = Backtester(1000, transaction_cost=0)
    cost = Backtester(1000, transaction_cost=0.01)

    pnl_no_cost = no_cost.run(sample_df())["trade_history"]["Trade_PnL"].iloc[0]
    pnl_cost = cost.run(sample_df())["trade_history"]["Trade_PnL"].iloc[0]

    assert pnl_cost < pnl_no_cost


def test_forced_liquidation():
    dates = pd.date_range("2024-01-01", periods=4)

    df = pd.DataFrame(
        {
            "Close": [100, 110, 120, 130],
            "Signal": [0, 1, 1, 1],
        },
        index=dates,
    )

    bt = Backtester(1000)
    result = bt.run(df)

    assert len(result["trade_history"]) == 1


def test_reconciliation():
    bt = Backtester(1000, transaction_cost=0)

    result = bt.run(sample_df())

    final_value = result["equity_curve"]["Portfolio_Value"].iloc[-1]
    pnl_sum = result["trade_history"]["Trade_PnL"].sum()

    assert final_value == pytest.approx(1000 + pnl_sum)


def test_no_trade_scenario():
    dates = pd.date_range("2024-01-01", periods=5)

    df = pd.DataFrame(
        {
            "Close": [100, 101, 102, 103, 104],
            "Signal": [0, 0, 0, 0, 0],
        },
        index=dates,
    )

    bt = Backtester(1000)

    result = bt.run(df)

    assert result["trade_history"].empty
    assert result["equity_curve"]["Portfolio_Value"].iloc[-1] == 1000

def test_empty_dataframe():
    bt = Backtester(1000)

    with pytest.raises(ValueError):
        bt.run(pd.DataFrame())

def test_multiple_trade_cycles():
    dates = pd.date_range("2024-01-01", periods=7)

    df = pd.DataFrame(
        {
            "Close": [100, 105, 110, 108, 115, 120, 118],
            "Signal": [0, 1, 1, 0, 1, 1, 0],
        },
        index=dates,
    )

    bt = Backtester(1000)

    result = bt.run(df)

    trades = result["trade_history"]

    assert len(trades) == 2

def test_reconciliation_with_transaction_costs():
    bt = Backtester(
        initial_capital=1000,
        transaction_cost=0.01,
    )

    result = bt.run(sample_df())

    final_value = result["equity_curve"]["Portfolio_Value"].iloc[-1]

    trade_pnl_sum = result["trade_history"]["Trade_PnL"].sum()

    assert final_value == pytest.approx(
        1000 + trade_pnl_sum,
        rel=1e-6,
    )
