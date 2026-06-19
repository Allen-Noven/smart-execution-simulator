# ====================================
# helpers.py
# ====================================

from datetime import datetime


# ====================================
# FORMAT PRICE
# ====================================

def format_price(price):

    if price is None:

        return None

    return round(float(price), 2)


# ====================================
# CURRENT TIMESTAMP
# ====================================

def get_current_time():

    return datetime.now()


# ====================================
# FORMAT TIMESTAMP
# ====================================

def format_timestamp(timestamp):

    if timestamp is None:

        return None

    return timestamp.strftime(

        "%Y-%m-%d %H:%M:%S"
    )


# ====================================
# CALCULATE NOTIONAL
# ====================================

def calculate_notional(

    qty,

    price

):

    if qty is None or price is None:

        return 0

    return qty * price


# ====================================
# CALCULATE SLIPPAGE
# ====================================

def calculate_slippage(

    arrival_price,

    fill_price

):

    if (

        arrival_price is None
        or
        fill_price is None

    ):

        return 0

    return (

        fill_price
        - arrival_price
    )


# ====================================
# CALCULATE BPS
# ====================================

def calculate_bps(

    arrival_price,

    fill_price

):

    if (

        arrival_price is None
        or
        fill_price is None
        or
        arrival_price == 0

    ):

        return 0

    return (

        (

            fill_price
            - arrival_price

        )

        / arrival_price

    ) * 10000


# ====================================
# CALCULATE PARTICIPATION RATE
# ====================================

def calculate_participation_rate(

    qty,

    market_volume

):

    if (

        market_volume is None
        or
        market_volume == 0

    ):

        return 0

    return qty / market_volume


# ====================================
# FORMAT ORDER LOG
# ====================================

def format_order_log(

    symbol,

    qty,

    status

):

    return (

        f"Symbol: {symbol} | "

        f"Qty: {qty} | "

        f"Status: {status}"
    )