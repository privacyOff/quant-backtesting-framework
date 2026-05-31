from abc import ABC, abstractmethod
from typing import Dict, Any

import pandas as pd


class BaseStrategy(ABC):
    """
    Abstract base class for all trading strategies.

    Every strategy must:

    1. Define a name
    2. Define parameters
    3. Implement generate_signals()
    """

    def __init__(
        self,
        name: str,
        parameters: Dict[str, Any] | None = None,
    ):
        self.name = name
        self.parameters = parameters or {}

    @abstractmethod
    def generate_signals(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Generate trading signals.

        Parameters
        ----------
        data : pd.DataFrame
            Market data for a single asset.

        Returns
        -------
        pd.DataFrame
            Original DataFrame plus Signal column.

        Signal Convention
        -----------------
        1  = Long
        0  = Flat
        -1 = Short
        """
        pass