from datetime import datetime
from pathlib import Path
from typing import cast, Any
from dotenv import load_dotenv
import os
import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit


def getData(
    symbol: str, start_date: datetime, end_date: datetime, time_frame: str
) -> pd.DataFrame:
    """
    Fetch historical market data for a symbol and save it as a CSV

    Parameters:
        symbol (str): Ticker we want to fetch (e.g. "AAPL").
        start_date (datetime): Start date/time for historical data.
        end_date (datetime): End date/time for historical data.
        time_frame (str): Bar granularity (e.g. "1Min", "Day").

    Returns:
        pd.DataFrame: historical bars with columns like
            [symbol, timestamp, open, high, low, close, volume, ...].
        .csv file: saved automatically in /data, name is "{symbol}_{timelength}.csv"
    """
    load_dotenv()
    API_KEY = os.environ["APCA_API_KEY_ID"]
    SECRET_KEY = os.environ["APCA_API_SECRET_KEY"]

    TIMEFRAME_MAP = {
        "1Min": TimeFrame(1, TimeFrameUnit("Min")),
        "1Hour": TimeFrame(1, TimeFrameUnit("Hour")),
        "1Day": TimeFrame(1, TimeFrameUnit("Day")),
    }

    tf = TIMEFRAME_MAP.get(time_frame)
    if tf is None:
        valid = ", ".join(TIMEFRAME_MAP.keys())
        raise ValueError(
            f"Invalid time_frame '{time_frame}'. Valid options are: {valid}"
        )

    client = StockHistoricalDataClient(API_KEY, SECRET_KEY)
    request_params = StockBarsRequest(
        symbol_or_symbols=[symbol],
        timeframe=tf,
        start=start_date,
        end=end_date,
    )

    bars = client.get_stock_bars(request_params)
    bars = cast(Any, bars)
    df = bars.df

    base_folder = Path("./data") / time_frame
    base_folder.mkdir(parents=True, exist_ok=True)
    filename = f"{symbol}_{time_frame}_{start_date:%Y-%m-%d}_{end_date:%Y-%m-%d}.csv"
    full_path = str(base_folder / filename)
    df.to_csv(full_path, index=True)
    print(f"Saved CSV to: {full_path}")

    return df
