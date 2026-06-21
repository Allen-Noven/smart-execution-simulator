from strategies.twap import TWAPStrategy

from execution.oms import OMS

from execution.execution_log import (
    ExecutionAuditLogger
)

from execution.fill_tracker import (
    FillTracker
)

from analytics.analytics import (
    ExecutionAnalytics
)

from analytics.slippage_analyzer import (
    SlippageAnalyzer
)

from analytics.pnl_tracker import (
    PnLTracker
)

from risk.risk_manager import (
    RiskManager
)

from risk.liquidity_monitor import (
    LiquidityMonitor
)

from core.market_state import (
    MarketState
)

from core.parent_order import (
    ParentOrder
)

from core.redis_state import (
    RedisState
)

from data.market_event_bus import (
    MarketEventBus
)

from data.replay import (
    MarketReplay
)

from data.real_time_data_loader import (
    RealTimeDataLoader
)

from utils.constants import (
    BUY
)

from utils.config import (

    DEFAULT_SYMBOL,

    EXECUTION_INTERVAL,

    DATA_MODE
)

import time


def start_execution_engine():

    # ====================================
    # EVENT BUS
    # ====================================

    event_bus = (
        MarketEventBus()
    )

    # ====================================
    # INITIALIZE SHARED MARKET STATE
    # ====================================

    market_state = (
        MarketState()
    )

    # ====================================
    # INITIALIZE REDIS STATE
    # ====================================

    redis_state = (
        RedisState()
    )

    # ====================================
    # INITIALIZE ALERTS
    # ====================================

    redis_state.set_alerts([])

    # ====================================
    # INITIALIZE MARKET DATA SOURCE
    # ====================================

    if DATA_MODE == "replay":

        market_data_source = (

            MarketReplay(

                data_path=
                "data/nvda_data.csv",

                market_state=
                market_state,

                event_bus=
                event_bus
            )
        )

    elif DATA_MODE == "live":

        market_data_source = (

            RealTimeDataLoader(

                market_state=
                market_state
            )
        )

    else:

        market_data_source = None

    # ====================================
    # INITIALIZE OMS
    # ====================================

    oms = OMS()

    # ====================================
    # INITIALIZE LOGGER
    # ====================================

    logger = (
        ExecutionAuditLogger()
    )

    # ====================================
    # INITIALIZE FILL TRACKER
    # ====================================

    fill_tracker = (
        FillTracker()
    )

    # ====================================
    # INITIALIZE ANALYTICS COMPONENTS
    # ====================================

    slippage_analyzer = (
        SlippageAnalyzer()
    )

    pnl_tracker = (
        PnLTracker()
    )

    # ====================================
    # INITIALIZE ANALYTICS
    # ====================================

    analytics = (

        ExecutionAnalytics(

            slippage_analyzer=
            slippage_analyzer,

            pnl_tracker=
            pnl_tracker
        )
    )

    # ====================================
    # INITIALIZE RISK MANAGER
    # ====================================

    risk_manager = (

        RiskManager(

            market_state=
            market_state
        )
    )

    # ====================================
    # INITIALIZE LIQUIDITY MONITOR
    # ====================================

    liquidity_monitor = (

        LiquidityMonitor(

            market_state=
            market_state
        )
    )

    # ====================================
    # INITIALIZE PARENT ORDER
    # ====================================

    parent_order = (

        ParentOrder(

            symbol=
            DEFAULT_SYMBOL,

            side=
            BUY,

            quantity=
            5,

            strategy=
            "TWAP"
        )
    )

    parent_order.show()

    # ====================================
    # INITIALIZE EXECUTION STRATEGY
    # ====================================

    if parent_order.strategy == "TWAP":

        strategy = (

            TWAPStrategy(

                total_qty=
                parent_order.total_qty,

                total_minutes=
                1,

                slices=
                5
            )
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
    # SYNC MARKET STATE TO REDIS
    # ====================================

    redis_state.set_market_state(

        DEFAULT_SYMBOL,

        {

            "price":
            market_state.current_price,

            "spread":
            market_state.spread,

            "volume":
            market_state.current_volume,

            "liquidity":
            market_state.liquidity_score,

            "bid":
            market_state.bid_price,

            "ask":
            market_state.ask_price,

            "volatility":
            market_state.volatility
        }
    )

    # ====================================
    # START MARKET DATA FLOW
    # ====================================

    print(

        "\nStarting Market Data Source...\n"
    )

    # ====================================
    # REPLAY MODE
    # ====================================

    if DATA_MODE == "replay":

        print(

            "Replay Mode Enabled.\n"
        )

        market_data_source.run()

    # ====================================
    # LIVE MODE
    # ====================================

    elif DATA_MODE == "live":

        print(

            "Live Market Feed Enabled.\n"
        )

        market_data_source.run(
            DEFAULT_SYMBOL
        )

    # ====================================
    # EXECUTION STATUS
    # ====================================

    redis_state.set_execution_status(

        {

            "status":
            "RUNNING",

            "halted":
            False,

            "reason":
            None
        }
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

            f"Evaluating child order: "
            f"{qty} shares"
        )

        # ====================================
        # LIQUIDITY CHECK
        # ====================================

        liquidity_result = (
            liquidity_monitor.evaluate_market()
        )

        if (

            liquidity_result[
                "market_quality"
            ] == "POOR"

        ):

            redis_state.set_alerts(

                [

                    "Liquidity Conditions Failed"
                ]
            )

            print(

                "\nLiquidity Check Failed.\n"
            )

            continue

        else:

            print(

                f"Liquidity OK | "

                f"Score: "

                f"{liquidity_result['liquidity_score']}"
            )

        # ====================================
        # RISK CHECK
        # ====================================

        risk_ok = (

            risk_manager.validate_order(

                qty=qty,

                current_position=
                current_position
            )
        )

        if not risk_ok:

            redis_state.set_alerts(

                [

                    "Risk Manager Rejected Order"
                ]
            )

            print(

                "\nRisk Check Failed.\n"
            )

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

        order = (

            oms.submit_market_order(

                symbol=
                parent_order.symbol,

                qty=
                qty,

                side=
                parent_order.side
            )
        )

        # ====================================
        # ORDER FAILURE
        # ====================================

        if order is None:

            redis_state.set_alerts(

                [

                    "OMS Order Submission Failed"
                ]
            )

            continue

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

            symbol=
            parent_order.symbol,

            qty=
            qty,

            strategy=
            parent_order.strategy,

            order_response=
            order
        )

        # ====================================
        # TRACK FILLS
        # ====================================

        fill_tracker.record_fill(

            order_id=
            str(order.id),

            symbol=
            parent_order.symbol,

            qty=
            qty,

            fill_price=
            fill_price,

            status=
            str(order.status)
        )

        # ====================================
        # SYNC FILLS TO REDIS
        # ====================================

        redis_state.set_fills(

            fill_tracker.fills
        )

        # ====================================
        # RECORD SLIPPAGE
        # ====================================

        slippage_analyzer.record_execution(

            symbol=
            parent_order.symbol,

            side=
            BUY,

            qty=
            qty,

            arrival_price=
            arrival_price,

            fill_price=
            fill_price
        )

        # ====================================
        # UPDATE PNL
        # ====================================

        pnl_tracker.record_trade(

            side=
            BUY,

            qty=
            qty,

            fill_price=
            fill_price
        )

        # ====================================
        # EXECUTION SUMMARY
        # ====================================

        execution_summary = {

            "strategy":
            parent_order.strategy,

            "filled_qty":
            current_position,

            "remaining_qty":
            (

                parent_order.total_qty
                -
                current_position
            ),

            "completion":
            round(

                current_position
                /
                parent_order.total_qty
                * 100,

                2
            )
        }

        # ====================================
        # SYNC EXECUTION SUMMARY
        # ====================================

        redis_state.set_execution_summary(
            execution_summary
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
    # EXECUTION COMPLETED STATUS
    # ====================================

    redis_state.set_execution_status(

        {

            "status":
            "COMPLETED",

            "halted":
            False,

            "reason":
            None
        }
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

    slippage_analyzer.show_summary()

    pnl_tracker.show_summary()

    # ====================================
    # RETURN RESULT
    # ====================================

    return {

        "status":
        "COMPLETED",

        "fills":
        fill_tracker.fills,

        "analytics":
        analytics.get_execution_summary()
    }


if __name__ == "__main__":

    start_execution_engine()