from strategies.twap import TWAPStrategy

from oms import OMS

from execution_log import ExecutionLogger

from fill_tracker import FillTracker

from analytics import ExecutionAnalytics

from risk_manager import RiskManager

from liquidity_monitor import (
    LiquidityMonitor
)

from market_state import MarketState

from replay import MarketReplay

from real_time_data_loader import (
    RealTimeDataLoader
)

from parent_order import ParentOrder

from alpaca.trading.enums import (
    OrderSide
)

from utils.config import (

    DEFAULT_SYMBOL,

    EXECUTION_INTERVAL,

    DATA_MODE
)

import time


# ====================================
# INITIALIZE SHARED MARKET STATE
# ====================================

market_state = MarketState()


# ====================================
# INITIALIZE MARKET DATA SOURCE
# ====================================

if DATA_MODE == "replay":

    market_data_source = MarketReplay(

        data_path="data/nvda_data.csv",

        market_state=market_state
    )

elif DATA_MODE == "live":

    market_data_source = (
        RealTimeDataLoader(

            market_state=market_state
        )
    )


# ====================================
# INITIALIZE OMS
# ====================================

oms = OMS()


# ====================================
# INITIALIZE LOGGER
# ====================================

logger = ExecutionLogger()


# ====================================
# INITIALIZE FILL TRACKER
# ====================================

fill_tracker = FillTracker()


# ====================================
# INITIALIZE ANALYTICS
# ====================================

analytics = ExecutionAnalytics()


# ====================================
# INITIALIZE RISK MANAGER
# ====================================

risk_manager = RiskManager(

    market_state=market_state
)


# ====================================
# INITIALIZE LIQUIDITY MONITOR
# ====================================

liquidity_monitor = (
    LiquidityMonitor(

        market_state=market_state
    )
)


# ====================================
# INITIALIZE PARENT ORDER
# ====================================

parent_order = ParentOrder(

    symbol=DEFAULT_SYMBOL,

    side=OrderSide.BUY,

    total_qty=5,

    strategy="TWAP",

    urgency="NORMAL",

    participation_limit=0.10
)

parent_order.show_order()


# ====================================
# INITIALIZE EXECUTION STRATEGY
# ====================================

if parent_order.strategy == "TWAP":

    strategy = TWAPStrategy(

        total_qty=parent_order.total_qty,

        total_minutes=1,

        slices=5
    )

    schedule = (
        strategy.generate_schedule()
    )

else:

    raise ValueError(

        f"Unsupported strategy: "
        f"{parent_order.strategy}"
    )


# ====================================
# CURRENT POSITION
# ====================================

current_position = 0


# ====================================
# INITIALIZE MARKET STATE
# ====================================

market_state.update(

    price=170,

    volume=50000,

    timestamp="09:30"
)


# ====================================
# START MARKET DATA FLOW
# ====================================

print(

    "\nStarting Market Data Source...\n"
)

# replay mode
if DATA_MODE == "replay":

    print(

        "Replay Mode Enabled.\n"
    )

# live mode
elif DATA_MODE == "live":

    print(

        "Live Market Feed Enabled.\n"
    )

    market_data_source.run(
        DEFAULT_SYMBOL
    )


# ====================================
# START EXECUTION
# ====================================

print(

    f"\nStarting "
    f"{parent_order.strategy} "
    f"Execution...\n"
)


# ====================================
# EXECUTION LOOP
# ====================================

for child_order in schedule:

    qty = child_order["qty"]

    print(

        f"Evaluating child order:"
        f" {qty} shares"
    )


    # ====================================
    # LIQUIDITY CHECK
    # ====================================

    liquidity_ok = (
        liquidity_monitor.evaluate_market()
    )

    if not liquidity_ok:

        continue


    # ====================================
    # RISK CHECK
    # ====================================

    risk_ok = (
        risk_manager.validate_order(

            qty=qty,

            current_position=current_position
        )
    )

    if not risk_ok:

        continue


    # ====================================
    # ARRIVAL PRICE
    # ====================================

    arrival_price = (
        market_state.current_price
    )


    # ====================================
    # SUBMIT ORDER
    # ====================================

    order = oms.submit_market_order(

        symbol=parent_order.symbol,

        qty=qty,

        side=parent_order.side
    )


    # ====================================
    # FILL PRICE
    # ====================================

    if order.filled_avg_price:

        fill_price = float(

            order.filled_avg_price
        )

    else:

        fill_price = arrival_price


    # ====================================
    # UPDATE POSITION
    # ====================================

    current_position += qty


    # ====================================
    # LOG EXECUTION
    # ====================================

    logger.log_execution(

        symbol=parent_order.symbol,

        qty=qty,

        strategy=parent_order.strategy,

        order_response=order
    )


    # ====================================
    # TRACK FILLS
    # ====================================

    fill_tracker.record_fill(

        order_id=str(order.id),

        symbol=parent_order.symbol,

        qty=qty,

        fill_price=fill_price,

        status=str(order.status)
    )


    # ====================================
    # RECORD ANALYTICS
    # ====================================

    analytics.record_fill(

        symbol=parent_order.symbol,

        strategy=parent_order.strategy,

        arrival_price=arrival_price,

        fill_price=fill_price,

        qty=qty
    )


    # ====================================
    # EXECUTION INTERVAL
    # ====================================

    time.sleep(
        EXECUTION_INTERVAL
    )


# ====================================
# EXECUTION COMPLETED
# ====================================

print(

    "\nExecution Completed.\n"
)


# ====================================
# SHOW EXECUTION LOGS
# ====================================

logger.show_logs()


# ====================================
# SHOW FILL REPORT
# ====================================

fill_tracker.show_fills()

fill_tracker.show_summary()


# ====================================
# SHOW ANALYTICS
# ====================================

analytics.show_summary()
