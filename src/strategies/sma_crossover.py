import pandas as pd
from typing import cast


def generate_sma_signal(
    df: pd.DataFrame,
    short_window: int = 9,
    long_window: int = 21,
) -> pd.Series:
    """
    Compute SMA crossover signals for a given DataFrame of historical prices

    Parameters:
        df (pd.DataFrame): Cleaned price data with 'close' column indexed by timestamp
        short_window (int): Period for short-term SMA
        long_window (int): Period for a long-term SMA

    Returns:
        pd.Series: Series of signals (+1 for buy, -1 for sell, 0 for hold) aligned
            to index
    """

    close = cast(pd.Series, df["close"])
    short_sma = close.rolling(window=short_window).mean()
    long_sma = close.rolling(window=long_window).mean()

    signals = pd.Series(index=df.index, dtype=float)

    signals.iloc[0] = 0

    for i in range(1, len(df)):
        prev_short = short_sma.iloc[i - 1]  # type: ignore
        prev_long = long_sma.iloc[i - 1]  # type: ignore

        curr_short = short_sma.iloc[i]  # type: ignore
        curr_long = long_sma.iloc[i]  # type: ignore

        # Bullish Crossover
        if prev_short <= prev_long and curr_short > curr_long:
            signals.iloc[i] = 1

        # Bearish Crossover
        elif prev_short >= prev_long and curr_short < curr_long:
            signals.iloc[i] = -1

        # No Crossover
        else:
            signals.iloc[i] = 0

    return signals
