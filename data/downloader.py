import logging
from typing import Dict, List

import pandas as pd
import yfinance as yf


logger = logging.getLogger(__name__)


REQUIRED_COLUMNS = [
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
]


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize yfinance output columns.

    Recent yfinance versions may return a MultiIndex
    even for a single ticker.

    Examples
    --------
    MultiIndex([
        ('Open', 'AAPL'),
        ('High', 'AAPL'),
        ...
    ])

    becomes:

    Index([
        'Open',
        'High',
        ...
    ])
    """

    if isinstance(df.columns, pd.MultiIndex):

        # Typical single-ticker structure
        if df.columns.nlevels == 2:
            df.columns = df.columns.get_level_values(0)

        else:
            raise ValueError(
                f"Unsupported MultiIndex structure: "
                f"{df.columns}"
            )

    return df


def validate_data(df: pd.DataFrame) -> bool:
    """
    Validate downloaded market data.

    Parameters
    ----------
    df : pd.DataFrame
        OHLCV market data.

    Returns
    -------
    bool
        True if data is valid.

    Raises
    ------
    ValueError
        If validation fails.
    """

    if df.empty:
        raise ValueError(
            "DataFrame is empty."
        )

    missing_columns = [
        col
        for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: "
            f"{missing_columns}"
        )

    if not df.index.is_monotonic_increasing:
        raise ValueError(
            "Date index is not sorted."
        )

    if df.index.duplicated().any():
        raise ValueError(
            "Duplicate dates found."
        )

    if df.isnull().values.any():
        raise ValueError(
            "Missing values detected."
        )

    if (df["Volume"] < 0).to_numpy().any():
        raise ValueError(
            "Negative volume values detected."
        )

    return True


def download_data(
    tickers: List[str],
    start_date: str,
    end_date: str,
) -> Dict[str, pd.DataFrame]:
    """
    Download historical market data.

    Parameters
    ----------
    tickers : list[str]
        List of ticker symbols.

    start_date : str
        Start date (YYYY-MM-DD).

    end_date : str
        End date (YYYY-MM-DD).

    Returns
    -------
    dict[str, pd.DataFrame]
        Dictionary mapping ticker symbols
        to validated DataFrames.
    """

    market_data: Dict[str, pd.DataFrame] = {}

    for ticker in tickers:

        try:
            logger.info(
                f"Downloading data for {ticker}"
            )

            df = yf.download(
                ticker,
                start=start_date,
                end=end_date,
                progress=False,
                auto_adjust=False,
                group_by="column",
            )

            if df.empty:
                logger.warning(
                    f"{ticker} could not be downloaded."
                )
                continue

            # Normalize columns from yfinance
            df = normalize_columns(df)

            # Keep only rows with complete data
            df = df.dropna()

            # Remove duplicate timestamps
            df = df[
                ~df.index.duplicated(
                    keep="first"
                )
            ]

            # Ensure chronological ordering
            df = df.sort_index()

            validate_data(df)

            market_data[ticker] = df

            logger.info(
                f"{ticker}: "
                f"{len(df)} rows downloaded."
            )

        except Exception:
            logger.exception(
                f"Failed to process {ticker}"
            )

    return market_data