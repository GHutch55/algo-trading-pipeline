import pandas as pd
from typing import cast


def generate_mr_signals(df: pd.DataFrame, window_size: int = 20) -> pd.Series:
    close = cast(pd.Series, df["close"])
    sma = close.rolling(window=window_size).mean()
    rolling_stddev = close.rolling(window=window_size).std()

    signals = pd.Series(index=df.index, dtype=float)

    signals.iloc[0] = 0

    for i in range(1, len(df)):
        z_score = (close.iloc[i] - sma.iloc[i]) / rolling_stddev.iloc[i]  # type: ignore

        if z_score >= 2:
            # BUY
            signals.iloc[i] = 1
        elif z_score <= -2:
            # SELL
            signals.iloc[i] = -1
        else:
            # HOLD
            signals.iloc[i] = 0

        # implement a stop-loss / risk management

    return signals
