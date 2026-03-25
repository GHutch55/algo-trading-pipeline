from typing import Optional, cast
from datetime import datetime
from backtest.portfolio import Portfolio
from backtest.execution import generate_order
import pandas as pd


class BacktestEngine:
    def __init__(
        self,
        initial_cash: float = 10000,
        commission_rate: float = 0.001,
        allocation_pct: float = 0.999,
        fill_timing: str = "next_open",  # 'same_close', 'next_open', 'next_close'
    ):
        """
        Initialize the backtesting engine.
        Parameters:
        initial_cash: Starting capital
        commission_rate: Commission as decimal (0.001 = 0.1%)
        allocation_pct: Fraction of cash to use per trade (0.999 = 99.9%)
        fill_timing: When orders fill relative to signal bar
            - 'same_close': Fill at signal bar close (unrealistic, but fast)
            - 'next_open': Fill at next bar open (realistic for market orders)
            - 'next_close': Fill at next bar close (conservative)
        """
        self.initial_cash = initial_cash
        self.commission_rate = commission_rate
        self.allocation_pct = allocation_pct
        self.fill_timing = fill_timing
        self.portfolio: Optional[Portfolio] = None

    def run(self, df: pd.DataFrame, signals: pd.Series):
        self.portfolio = Portfolio(self.initial_cash)

        if self.fill_timing == "next_open" or self.fill_timing == "next_close":
            loop_until = len(df) - 1
        else:
            loop_until = len(df)

        for i in range(loop_until):
            signal = signals.iloc[i]
            timestamp = cast(datetime, df.index[i])

            if self.fill_timing == "same_close":
                fill_price = df["close"].iloc[i]
            elif self.fill_timing == "next_open":
                fill_price = df["open"].iloc[i + 1]
            else:
                fill_price = df["close"].iloc[i + 1]

            trade = generate_order(
                signal,
                self.portfolio.get_position(),
                fill_price,
                timestamp,
                self.portfolio.get_cash(),
            )

            if trade:
                self.portfolio.apply_trade(trade)

            self.portfolio.update_market_value(df["close"].iloc[i], timestamp)

        if self.fill_timing != "same_close":
            final_price = df["close"].iloc[-1]
            final_timestamp = cast(datetime, df.index[-1])
            self.portfolio.update_market_value(final_price, final_timestamp)

        return self._build_results()

    def _build_results(self):
        assert self.portfolio is not None
        equity_df = pd.DataFrame(self.portfolio.equity_pos)
        trades_df = pd.DataFrame(self.portfolio.trade_history)

        final_value = self.portfolio.get_equity()
        total_return = (final_value - self.initial_cash) / self.initial_cash

        return {
            "portfolio": self.portfolio,
            "equity_curve": equity_df,
            "trades": trades_df,
            "final_value": final_value,
            "total_return": total_return,
            "initial_cash": self.initial_cash,
        }
