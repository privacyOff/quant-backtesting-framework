import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        self.tickers = [
            ticker.strip()
            for ticker in os.getenv("TICKERS", "AAPL").split(",")
            if ticker.strip()
        ]

        self.start_date = os.getenv("START_DATE", "2020-01-01")
        self.end_date = os.getenv("END_DATE", "2025-01-01")

        self.initial_capital = float(
            os.getenv("INITIAL_CAPITAL", 100000)
        )

        self.transaction_cost = float(
            os.getenv("TRANSACTION_COST", 0.001)
        )

        self.position_size = float(
            os.getenv("POSITION_SIZE", 1.0)
        )

        self._validate()

    def _validate(self):
        if not self.tickers:
            raise ValueError(
                "TICKERS must contain at least one ticker."
            )

        if self.initial_capital <= 0:
            raise ValueError(
                "INITIAL_CAPITAL must be greater than 0."
            )

        if not (0 <= self.transaction_cost <= 1):
            raise ValueError(
                "TRANSACTION_COST must be between 0 and 1."
            )

        if not (0 < self.position_size <= 1):
            raise ValueError(
                "POSITION_SIZE must be between 0 and 1."
            )

        start = datetime.strptime(
            self.start_date,
            "%Y-%m-%d"
        )

        end = datetime.strptime(
            self.end_date,
            "%Y-%m-%d"
        )

        if start >= end:
            raise ValueError(
                "START_DATE must be earlier than END_DATE."
            )


settings = Settings()