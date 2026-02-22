from datetime import datetime, timezone

from analysis.data import getData


def main():
    symbol = "AAPL"
    start_date = datetime(2026, 2, 2, 14, 30, tzinfo=timezone.utc)
    end_date = datetime(2026, 2, 2, 21, 0, tzinfo=timezone.utc)
    time_frame = "1Hour" # 1Min, 1Hour or 1Day

    df = getData(symbol, start_date, end_date, time_frame)

    print(df.head())
    print(df.columns)
    print(df.shape)


if __name__ == "__main__":
    main()
