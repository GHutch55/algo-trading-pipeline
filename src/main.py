from datetime import datetime, timezone
from analysis.data import get_data
from strategies.mean_reversion import generate_mr_signals

def main():
    symbol = "QQQ"
    start_date = datetime(2024, 10, 1, tzinfo=timezone.utc)
    end_date = datetime(2024, 12, 31, tzinfo=timezone.utc)
    time_frame = "1Min"  # 1Min, 1Hour or 1Day

    print(
        f"Fetching {symbol} {time_frame} date from {start_date.date()} to {end_date.date()}"
    )
    df = get_data(symbol, start_date, end_date, time_frame)
    print(f"Fetched {len(df)} bars")
    print(f"Date range: {df.index[0]} to {df.index[-1]}")


if __name__ == "__main__":
    main()
