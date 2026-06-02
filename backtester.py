import pandas as pd


class Backtester:
    def __init__(self, initial_capital, transaction_cost=0.0, position_size=1.0):
        if initial_capital <= 0:
            raise ValueError("initial_capital must be > 0")
        if not 0 <= transaction_cost <= 1:
            raise ValueError("transaction_cost must be between 0 and 1")
        if not 0 < position_size <= 1:
            raise ValueError("position_size must be between 0 and 1")

        self.initial_capital = float(initial_capital)
        self.transaction_cost = float(transaction_cost)
        self.position_size = float(position_size)

    def _validate_input(self, df):
        if df is None or df.empty:
            raise ValueError("Input DataFrame cannot be empty")

        required = {"Close", "Signal"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")

    def run(self, signal_df):
        self._validate_input(signal_df)

        df = signal_df.copy()

        df["Position"] = df["Signal"].shift(1).fillna(0).astype(int)

        cash = self.initial_capital
        shares = 0.0

        active_trade = None
        trades = []

        cash_series = []
        shares_series = []
        holdings_series = []
        portfolio_series = []

        position_change = df["Position"].diff().fillna(df["Position"])

        for idx, row in df.iterrows():
            close = float(row["Close"])
            change = position_change.loc[idx]

            if change == 1 and shares == 0:
                allocation = cash * self.position_size
                entry_cost = allocation * self.transaction_cost
                investable_amount = allocation - entry_cost

                purchased_shares = investable_amount / close if close > 0 else 0.0

                cash -= allocation
                shares += purchased_shares

                active_trade = {
                    "Entry_Date": idx,
                    "Entry_Price": close,
                    "Shares": purchased_shares,
                    "Entry_Cost": entry_cost,
                }

            elif change == -1 and shares > 0:
                gross_exit_value = shares * close
                exit_cost = gross_exit_value * self.transaction_cost
                net_exit_value = gross_exit_value - exit_cost

                cash += net_exit_value

                if active_trade is not None:
                    gross_pnl = (
                        (close - active_trade["Entry_Price"])
                        * active_trade["Shares"]
                    )

                    trade_pnl = (
                        gross_pnl
                        - active_trade["Entry_Cost"]
                        - exit_cost
                    )

                    invested_amount = (
                        active_trade["Entry_Price"]
                        * active_trade["Shares"]
                    )

                    gross_return = (
                        gross_pnl / invested_amount
                        if invested_amount > 0 else 0.0
                    )

                    net_return = (
                        trade_pnl / invested_amount
                        if invested_amount > 0 else 0.0
                    )

                    trades.append({
                        "Entry_Date": active_trade["Entry_Date"],
                        "Exit_Date": idx,
                        "Entry_Price": active_trade["Entry_Price"],
                        "Exit_Price": close,
                        "Shares": active_trade["Shares"],
                        "Gross_PnL": gross_pnl,
                        "Trade_PnL": trade_pnl,
                        "Gross_Return": gross_return,
                        "Net_Return": net_return,
                        "Holding_Period": (idx - active_trade["Entry_Date"]).days
                        if hasattr(idx - active_trade["Entry_Date"], "days")
                        else None,
                    })

                shares = 0.0
                active_trade = None

            holdings_value = shares * close
            portfolio_value = cash + holdings_value

            cash_series.append(cash)
            shares_series.append(shares)
            holdings_series.append(holdings_value)
            portfolio_series.append(portfolio_value)

        if shares > 0:
            idx = df.index[-1]
            close = float(df["Close"].iloc[-1])

            gross_exit_value = shares * close
            exit_cost = gross_exit_value * self.transaction_cost
            net_exit_value = gross_exit_value - exit_cost

            cash += net_exit_value

            gross_pnl = (
                (close - active_trade["Entry_Price"])
                * active_trade["Shares"]
            )

            trade_pnl = (
                gross_pnl
                - active_trade["Entry_Cost"]
                - exit_cost
            )

            invested_amount = (
                active_trade["Entry_Price"]
                * active_trade["Shares"]
            )

            trades.append({
                "Entry_Date": active_trade["Entry_Date"],
                "Exit_Date": idx,
                "Entry_Price": active_trade["Entry_Price"],
                "Exit_Price": close,
                "Shares": active_trade["Shares"],
                "Gross_PnL": gross_pnl,
                "Trade_PnL": trade_pnl,
                "Gross_Return": gross_pnl / invested_amount if invested_amount > 0 else 0.0,
                "Net_Return": trade_pnl / invested_amount if invested_amount > 0 else 0.0,
                "Holding_Period": (idx - active_trade["Entry_Date"]).days
                if hasattr(idx - active_trade["Entry_Date"], "days")
                else None,
            })

            portfolio_series[-1] = cash
            holdings_series[-1] = 0.0
            shares_series[-1] = 0.0
            cash_series[-1] = cash

        df["Cash"] = cash_series
        df["Shares"] = shares_series
        df["Holdings_Value"] = holdings_series
        df["Portfolio_Value"] = portfolio_series
        df["Daily_Return"] = df["Portfolio_Value"].pct_change().fillna(0.0)

        trades_df = pd.DataFrame(trades)

        return {
            "equity_curve": df,
            "trade_history": trades_df,
        }