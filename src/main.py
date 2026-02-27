from datetime import datetime, timezone

from analysis.data import get_data
from strategies.sma_crossover import generate_sma_signal
import pandas as pd


def main():
    symbol = "AAPL"
    start_date = datetime(2026, 2, 2, 14, 30, tzinfo=timezone.utc)
    end_date = datetime(2026, 2, 2, 21, 0, tzinfo=timezone.utc)
    time_frame = "1Min"  # 1Min, 1Hour or 1Day

    df = get_data(symbol, start_date, end_date, time_frame)

    res = generate_sma_signal(df)
    pd.set_option("display.max_rows", None)
    print(res)


if __name__ == "__main__":
    main()
