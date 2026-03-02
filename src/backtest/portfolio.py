from datetime import datetime
from typing import Dict, List


class Portfolio:
    """
    Represents a single-asset trading portfolio.

    Tracks:
    - Available cash
    - Current position (share quantity)
    - Current total equity
    - Equity history over time
    - Trade history

    Equity is always defined as:

        equity = cash + (position * current_price)
    """

    def __init__(self, initial_cash: float):
        """
        Initialize the portfolio with starting capital.

        Parameters:
            initial_cash (float): Starting cash balance.
        """
        self.cash: float = initial_cash
        self.position: int = 0  # Number of shares currently held
        self.current_equity: float = initial_cash

        # Historical logs
        self.equity_pos: List[Dict] = []
        self.trade_history: List[Dict] = []

    def apply_trade(self, trade: Dict) -> None:
        """
        Apply a completed trade to the portfolio.

        The trade dictionary must contain:

            {
                "timestamp": datetime,
                "side": "buy" | "sell",
                "quantity": int,
                "price": float,
                "gross_value": float,
                "commission": float,
                "net_cash_change": float
            }

        Effects:
        - Updates cash balance
        - Updates position quantity
        - Appends trade to trade history

        Parameters:
            trade (dict): Executed trade details.
        """

        # Update cash
        self.cash += trade["net_cash_change"]

        # Update position quantity
        if trade["side"] == "buy":
            self.position += trade["quantity"]
        elif trade["side"] == "sell":
            self.position -= trade["quantity"]

        # Log trade
        self.trade_history.append(trade)

    def update_market_value(self, current_price: float, timestamp: datetime) -> None:
        """
        Update portfolio equity based on the latest market price.

        This should be called at every timestep in the backtest loop.

        Parameters:
            current_price (float): Latest asset price.
            timestamp (datetime): Current market timestamp.
        """

        market_value = self.position * current_price
        equity = self.cash + market_value

        self.current_equity = equity

        snapshot = {
            "timestamp": timestamp,
            "cash": self.cash,
            "position": self.position,
            "price": current_price,
            "market_value": market_value,
            "equity": equity,
        }

        self.equity_pos.append(snapshot)

    def get_equity(self) -> float:
        """
        Returns:
            float: Current total portfolio equity.
        """
        return self.current_equity

    def get_cash(self) -> float:
        """
        Returns:
            float: Current available cash balance.
        """
        return self.cash

    def get_position(self) -> int:
        """
        Returns:
            int: Current share quantity held.
        """
        return self.position
