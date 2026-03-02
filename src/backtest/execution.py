from datetime import datetime


def generate_order(
    signal: int,
    current_position: int,
    current_price: float,
    timestamp: datetime,
    cash: float,
):
    """
    Generate a trade order based on signal and current portfolio state (long-only).

    Decision Logic:
    - FLAT (position = 0) + signal= 1 → BUY using 99.9% of available cash
    - LONG (position > 0) + signal= -1 → SELL entire position
    - All other cases → No trade (returns None)

    Commission: 0.1% (0.001) applied to gross trade value.

    Returns trade dictionary on execution:
        {
            "timestamp": datetime,
            "side": "buy" | "sell",
            "quantity": int,
            "price": float,
            "gross_value": float,
            "commission": float,
            "net_cash_change": float (negative for buy, positive for sell)
        }

    Parameters:
        signal (int): Trading signal (+1=buy, -1=sell, 0=hold)
        current_position (int): Current number of shares held
        current_price (float): Current market price per share
        timestamp (datetime): Current market timestamp
        cash (float): Available cash balance

    Returns:
        dict | None: Trade dictionary if order generated, None otherwise
    """
    if current_position == 0:  # flat
        if signal == 1:
            qty = int((cash * 0.999) / current_price)

            if qty < 1:
                return None

            gross_value = qty * current_price
            commission = gross_value * 0.001

            trade = {
                "timestamp": timestamp,
                "side": "buy",
                "quantity": qty,
                "price": current_price,
                "gross_value": gross_value,
                "commission": commission,
                "net_cash_change": -(gross_value + commission),
            }

            return trade

    elif current_position > 0:  # long
        if signal == -1:
            gross_value = current_position * current_price
            commission = gross_value * 0.001

            trade = {
                "timestamp": timestamp,
                "side": "sell",
                "quantity": current_position,
                "price": current_price,
                "gross_value": gross_value,
                "commission": commission,
                "net_cash_change": gross_value - commission,
            }

            return trade

    return None
