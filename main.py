# from config import settings
# from data.downloader import download_data


# import logging

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(levelname)s - %(message)s"
# )


# def main():

#     market_data = download_data(
#         settings.tickers,
#         settings.start_date,
#         settings.end_date,
#     )

#     for ticker, df in market_data.items():
#         print(f"\n{ticker}")
#         print(df.head())


# if __name__ == "__main__":
#     main()








import logging

from config import settings
from data.downloader import download_data


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
)


def main():

    market_data = download_data(
        settings.tickers,
        settings.start_date,
        settings.end_date,
    )

    print(
        f"\nSuccessfully loaded "
        f"{len(market_data)} assets."
    )

    for ticker, df in market_data.items():

        print(f"\n{'=' * 60}")
        print(ticker)
        print(f"{'=' * 60}")

        print("\nColumns:")
        print(df.columns.tolist())

        print("\nHead:")
        print(df.head())

        print("\nShape:")
        print(df.shape)


if __name__ == "__main__":
    main()