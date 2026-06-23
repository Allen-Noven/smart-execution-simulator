# ====================================
# execution_service.py
# ====================================
from storage.order_repository import (
    OrderRepository
)

from core.redis_state import (
    RedisState
)


from storage.fill_repository import (
    FillRepository
)

from storage.position_repository import (
    PositionRepository
)

from strategies.twap import (
    TWAPStrategy
)

from strategies.adaptive_vwap import (
    AdaptiveVWAPStrategy
)

from strategies.pov import (
    POVStrategy
)

from execution.execution_scheduler import (
    ExecutionScheduler
)

from execution.oms.live_oms import (
    LiveOMS
)

from execution.fill_tracker import (
    FillTracker
)

from execution.execution_log import (
    ExecutionAuditLogger
)

from analytics.slippage_analyzer import (
    SlippageAnalyzer
)

from analytics.pnl_tracker import (
    PnLTracker
)

from storage.execution_repository import (
    ExecutionRepository
)

from data.market_event_bus import (
    MarketEventBus
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

from portfolio.position_manager import (
    PositionManager
)

from utils.logger import (
    SystemLogger
)

from utils.constants import (

    TWAP,

    VWAP,

    POV,

    RUNNING,

    HALTED,

    COMPLETED,

    ORDER_FILLED_EVENT,

    EXECUTION_STARTED,

    EXECUTION_COMPLETED
)

from utils.config import (

    EXECUTION_INTERVAL,

    DEFAULT_PARTICIPATION
)


class ExecutionService:


    # ====================================
    # INIT
    # ====================================

    def __init__(
        

        self,

        market_state=None,

        event_bus=None,

        oms=None,

        position_manager=None
    ):

        # ====================================
        # LOGGER
        # ====================================

        self.order_repository = (
            OrderRepository()
        )
        
        self.fill_repository = (
            FillRepository()
        )

        self.position_repository = (
            PositionRepository()
        )
        self.redis_state = (
    RedisState()
)


        self.logger = (
            SystemLogger()
        )

        # ====================================
        # MARKET STATE
        # ====================================

        self.market_state = (

            market_state
            if market_state
            else MarketState()
        )

        # ====================================
        # EVENT BUS
        # ====================================

        self.event_bus = (

            event_bus
            if event_bus
            else MarketEventBus()
        )

        # ====================================
        # OMS
        # ====================================

        self.oms = (

            oms
            if oms
            else LiveOMS()
        )

        # ====================================
        # EXECUTION LOGGER
        # ====================================

        self.execution_logger = (
            ExecutionAuditLogger()
        )

        # ====================================
        # FILL TRACKER
        # ====================================

        self.fill_tracker = (
            FillTracker()
        )

        # ====================================
        # ANALYTICS
        # ====================================

        self.slippage_analyzer = (
            SlippageAnalyzer()
        )

        self.pnl_tracker = (
            PnLTracker()
        )

        # ====================================
        # POSITION MANAGER
        # ====================================

        self.position_manager = (

            position_manager
            if position_manager
            else PositionManager()
        )

        # ====================================
        # EXECUTION REPOSITORY
        # ====================================

        self.execution_repository = (
            ExecutionRepository()
        )

        # ====================================
        # RISK MANAGER
        # ====================================

        self.risk_manager = (

            RiskManager(

                market_state=
                self.market_state
            )
        )

        # ====================================
        # LIQUIDITY MONITOR
        # ====================================

        self.liquidity_monitor = (

            LiquidityMonitor(

                market_state=
                self.market_state
            )
        )

        # ====================================
        # ACTIVE ORDERS
        # ====================================

        self.active_orders = {}

        # ====================================
        # STATUS
        # ====================================

        self.status = RUNNING

        self.logger.info(
            "Execution Service Initialized"
        )

# ====================================
# execution_service.py
# ====================================

from storage.order_repository import (
    OrderRepository
)

from storage.fill_repository import (
    FillRepository
)

from storage.position_repository import (
    PositionRepository
)

from strategies.twap import (
    TWAPStrategy
)

from strategies.adaptive_vwap import (
    AdaptiveVWAPStrategy
)

from strategies.pov import (
    POVStrategy
)

from execution.execution_scheduler import (
    ExecutionScheduler
)

from execution.oms.live_oms import (
    LiveOMS
)

from execution.fill_tracker import (
    FillTracker
)

from execution.execution_log import (
    ExecutionAuditLogger
)

from analytics.slippage_analyzer import (
    SlippageAnalyzer
)

from analytics.pnl_tracker import (
    PnLTracker
)

from storage.execution_repository import (
    ExecutionRepository
)

from data.market_event_bus import (
    MarketEventBus
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

from portfolio.position_manager import (
    PositionManager
)

from utils.logger import (
    SystemLogger
)

from utils.constants import (

    TWAP,

    VWAP,

    POV,

    RUNNING,

    HALTED,

    COMPLETED,

    ORDER_FILLED_EVENT,

    EXECUTION_STARTED,

    EXECUTION_COMPLETED
)

from utils.config import (

    EXECUTION_INTERVAL,

    DEFAULT_PARTICIPATION
)


class ExecutionService:


    # ====================================
    # INIT
    # ====================================

    def __init__(

        self,

        market_state=None,

        event_bus=None,

        oms=None,

        position_manager=None
    ):

        self.order_repository = (
            OrderRepository()
        )

        self.fill_repository = (
            FillRepository()
        )

        self.position_repository = (
            PositionRepository()
        )

        self.logger = (
            SystemLogger()
        )

        # ====================================
        # MARKET STATE
        # ====================================

        self.market_state = (

            market_state
            if market_state
            else MarketState()
        )

        # ====================================
        # EVENT BUS
        # ====================================

        self.event_bus = (

            event_bus
            if event_bus
            else MarketEventBus()
        )

        # ====================================
        # OMS
        # ====================================

        self.oms = (

            oms
            if oms
            else LiveOMS()
        )

        # ====================================
        # EXECUTION LOGGER
        # ====================================

        self.execution_logger = (
            ExecutionAuditLogger()
        )

        # ====================================
        # FILL TRACKER
        # ====================================

        self.fill_tracker = (
            FillTracker()
        )

        # ====================================
        # ANALYTICS
        # ====================================

        self.slippage_analyzer = (
            SlippageAnalyzer()
        )

        self.pnl_tracker = (
            PnLTracker()
        )

        # ====================================
        # POSITION MANAGER
        # ====================================

        self.position_manager = (

            position_manager
            if position_manager
            else PositionManager()
        )

        # ====================================
        # EXECUTION REPOSITORY
        # ====================================

        self.execution_repository = (
            ExecutionRepository()
        )

        # ====================================
        # RISK MANAGER
        # ====================================

        self.risk_manager = (

            RiskManager(

                market_state=
                self.market_state
            )
        )

        # ====================================
        # LIQUIDITY MONITOR
        # ====================================

        self.liquidity_monitor = (

            LiquidityMonitor(

                market_state=
                self.market_state
            )
        )

        # ====================================
        # ACTIVE ORDERS
        # ====================================

        self.active_orders = {}

        # ====================================
        # STATUS
        # ====================================

        self.status = RUNNING

        self.logger.info(
            "Execution Service Initialized"
        )


    # ====================================
    # SUBMIT ORDER
    # ====================================

    def submit_order(

        self,

        parent_order
    ):

        try:

            # ====================================
            # START ORDER
            # ====================================

            parent_order.start_order()

            # ====================================
            # SAVE ORDER
            # ====================================

            self.order_repository.save_order(
                parent_order
            )

            # ====================================
            # STORE ACTIVE ORDER
            # ====================================

            self.active_orders[
                parent_order.order_id
            ] = parent_order

            # ====================================
            # LOG
            # ====================================

            self.logger.info(

                f"Execution Started | "

                f"{parent_order.symbol} | "

                f"{parent_order.strategy}"
            )

            # ====================================
            # EXECUTION START EVENT
            # ====================================

            self.event_bus.publish(

                EXECUTION_STARTED,

                parent_order.get_snapshot()
            )

            # ====================================
            # ORDER UPDATE
            # ====================================

            self.event_bus.publish(

                "ORDER_UPDATE",

                {

                    "order_id":
                    parent_order.order_id,

                    "symbol":
                    parent_order.symbol,

                    "status":
                    parent_order.status
                }
            )

            # ====================================
            # CREATE STRATEGY
            # ====================================

            strategy = (
                self.create_strategy(
                    parent_order
                )
            )

            # ====================================
            # GENERATE SCHEDULE
            # ====================================

            if hasattr(

                strategy,

                "generate_schedule"
            ):

                schedule = (
                    strategy.generate_schedule()
                )

            else:

                schedule = []

                while (

                    strategy.remaining_qty > 0
                ):

                    next_order = (

                        strategy.get_next_order()
                    )

                    if next_order is None:

                        break

                    schedule.append(
                        next_order
                    )

            # ====================================
            # EXECUTION SCHEDULER
            # ====================================

            scheduler = (

                ExecutionScheduler(

                    execution_interval=
                    EXECUTION_INTERVAL,

                    market_state=
                    self.market_state
                )
            )

            # ====================================
            # RUN EXECUTION
            # ====================================

            scheduler.run_schedule(

                schedule,

                lambda child_order:
                self.execute_child_order(

                    parent_order,

                    child_order
                )
            )

            # ====================================
            # COMPLETE ORDER
            # ====================================

            parent_order.complete_order()

            # ====================================
            # SAVE COMPLETED ORDER
            # ====================================

            self.order_repository.save_order(
                parent_order
            )

            # ====================================
            # SAVE EXECUTION
            # ====================================

            self.execution_repository.save_execution(

                parent_order.get_snapshot()
            )

            # ====================================
            # EXECUTION COMPLETED EVENT
            # ====================================

            self.event_bus.publish(

                EXECUTION_COMPLETED,

                parent_order.get_snapshot()
            )

            # ====================================
            # ORDER UPDATE
            # ====================================

            self.event_bus.publish(

                "ORDER_UPDATE",

                {

                    "order_id":
                    parent_order.order_id,

                    "symbol":
                    parent_order.symbol,

                    "status":
                    COMPLETED
                }
            )

            # ====================================
            # REMOVE ACTIVE ORDER
            # ====================================

            self.active_orders.pop(

                parent_order.order_id,

                None
            )

            # ====================================
            # LOG
            # ====================================

            self.logger.info(

                f"Execution Completed | "

                f"{parent_order.symbol}"
            )

            return {

                "status":
                COMPLETED,

                "order_id":
                parent_order.order_id
            }

        except Exception as error:

            # ====================================
            # HALT ORDER
            # ====================================

            parent_order.halt_order(
                str(error)
            )

            # ====================================
            # RISK ALERT
            # ====================================

            self.event_bus.publish(

                "RISK_ALERT",

                {

                    "message":
                    str(error)
                }
            )

            # ====================================
            # ORDER UPDATE
            # ====================================

            self.event_bus.publish(

                "ORDER_UPDATE",

                {

                    "order_id":
                    parent_order.order_id,

                    "symbol":
                    parent_order.symbol,

                    "status":
                    HALTED
                }
            )

            # ====================================
            # LOG
            # ====================================

            self.logger.error(

                f"Execution Failed | "

                f"{error}"
            )

            return {

                "status":
                HALTED,

                "reason":
                str(error)
            }
    # ====================================
    # EXECUTE CHILD ORDER
    # ====================================

    def execute_child_order(

        self,

        parent_order,

        child_order
    ):

        # ====================================
        # QTY
        # ====================================

        qty = child_order["qty"]

        # ====================================
        # LIQUIDITY CHECK
        # ====================================

        liquidity_result = (

            self.liquidity_monitor
            .evaluate_market()
        )

        if (

            liquidity_result[
                "market_quality"
            ] == "POOR"

        ):

            self.logger.warning(
                "Liquidity Check Failed"
            )

            self.event_bus.publish(

                "RISK_ALERT",

                {

                    "message":
                    "Liquidity Conditions Failed"
                }
            )

            return

        # ====================================
        # RISK CHECK
        # ====================================

        risk_ok = (

            self.risk_manager
            .validate_order(

                qty=qty,

                current_position=
                parent_order.filled_quantity
            )
        )

        if not risk_ok:

            self.logger.warning(
                "Risk Check Failed"
            )

            self.event_bus.publish(

                "RISK_ALERT",

                {

                    "message":
                    "Risk Check Failed"
                }
            )

            return

        # ====================================
        # ARRIVAL PRICE
        # ====================================

        arrival_price = (
            self.market_state.current_price
        )

        # ====================================
        # SEND TO OMS
        # ====================================

        order = (

            self.oms.submit_market_order(

                symbol=
                parent_order.symbol,

                qty=
                qty,

                side=
                parent_order.side
            )
        )

        # ====================================
        # OMS FAILURE
        # ====================================

        if order is None:

            self.logger.error(
                "OMS Submission Failed"
            )

            self.event_bus.publish(

                "RISK_ALERT",

                {

                    "message":
                    "OMS Submission Failed"
                }
            )

            return

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
        # UPDATE PARENT ORDER
        # ====================================

        parent_order.add_fill(

            fill_qty=qty,

            fill_price=fill_price
        )

        # ====================================
        # TRACK FILL
        # ====================================

        self.fill_tracker.record_fill(

            order_id=
            str(order.id),

            symbol=
            parent_order.symbol,

            qty=
            qty,

            fill_price=
            fill_price,

            status=
            str(order.status),

            side=
            parent_order.side,

            strategy=
            parent_order.strategy
        )
# ====================================
# SAVE FILL
# ====================================

        fill_data = {

            "order_id":
            str(order.id),

            "symbol":
            parent_order.symbol,

            "side":
            parent_order.side,

            "qty":
            qty,

            "fill_price":
            fill_price,

            "timestamp":
            str(parent_order.updated_at)
        }

        self.fill_repository.save_fill(
            fill_data
        )


        # ====================================
        # EXECUTION LOG
        # ====================================

        self.execution_logger.log_execution(

            symbol=
            parent_order.symbol,

            qty=
            qty,

            strategy=
            parent_order.strategy,

            order_response=
            order,

            side=
            parent_order.side,

            fill_price=
            fill_price
        )
        

        # ====================================
        # RECORD SLIPPAGE
        # ====================================

        self.slippage_analyzer.record_execution(

            symbol=
            parent_order.symbol,

            side=
            parent_order.side,

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

        self.pnl_tracker.record_trade(

            side=
            parent_order.side,

            qty=
            qty,

            fill_price=
            fill_price
        )

        # ====================================
        # UPDATE POSITION
        # ====================================

        self.position_manager.update_position(

            symbol=
            parent_order.symbol,

            side=
            parent_order.side,

            qty=
            qty,

            fill_price=
            fill_price,

            market_price=
            self.market_state.current_price
        )

        # ====================================
        # MARK TO MARKET
        # ====================================

        self.position_manager.mark_to_market(

            symbol=
            parent_order.symbol,

            market_price=
            self.market_state.current_price
        )


        # ====================================
        # POSITION SNAPSHOT
        # ====================================

        position_snapshot = (

            self.position_manager
            .get_position(

                parent_order.symbol
            )
        )

        # ====================================
        # SAVE POSITION
        # ====================================

        self.position_repository.save_position(
            position_snapshot
        )


        # ====================================
        # PORTFOLIO SUMMARY
        # ====================================

        portfolio_summary = (

            self.position_manager
            .get_portfolio_summary()
        )
# ====================================
        # REDIS POSITIONS
        # ====================================

        self.redis_state.set_positions(

            self.position_manager
            .get_all_positions()
        )

        # ====================================
        # REDIS PORTFOLIO
        # ====================================

        self.redis_state.set_portfolio_summary(

            portfolio_summary
        )

        # ====================================
        # REDIS EXECUTION STATUS
        # ====================================

        self.redis_state.set_execution_status(

            {

                "symbol":
                parent_order.symbol,

                "status":
                parent_order.status,

                "filled":
                parent_order.filled_quantity,

                "remaining":
                parent_order.remaining_quantity
            }
        )

        # ====================================
        # REDIS FILLS
        # ====================================

        self.redis_state.set_fills(

            self.fill_tracker.fills
        )

        # ====================================
        # FILLED EVENT
        # ====================================

        self.event_bus.publish(

            ORDER_FILLED_EVENT,

            {

                "order_id":
                parent_order.order_id,

                "symbol":
                parent_order.symbol,

                "side":
                parent_order.side,

                "qty":
                qty,

                "fill_price":
                fill_price
            }
        )

        # ====================================
        # FILL UPDATE
        # ====================================

        self.event_bus.publish(

            "FILL_UPDATE",

            {

                "order_id":
                parent_order.order_id,

                "symbol":
                parent_order.symbol,

                "qty":
                qty,

                "fill_price":
                fill_price
            }
        )

        # ====================================
        # POSITION UPDATE
        # ====================================

        self.event_bus.publish(

            "POSITION_UPDATE",

            {

                "position":
                position_snapshot,

                "portfolio":
                portfolio_summary
            }
        )

        # ====================================
        # ORDER UPDATE
        # ====================================

        self.event_bus.publish(

            "ORDER_UPDATE",

            {

                "order_id":
                parent_order.order_id,

                "symbol":
                parent_order.symbol,

                "status":
                parent_order.status
            }
        )

        # ====================================
        # LOG
        # ====================================

        self.logger.info(

            f"Child Order Executed | "

            f"{qty} @ {fill_price}"
        )


    # ====================================
    # CREATE STRATEGY
    # ====================================

    def create_strategy(

        self,

        parent_order
    ):

        if parent_order.strategy == TWAP:

            return TWAPStrategy(

                total_qty=
                parent_order.quantity,

                total_minutes=1,

                slices=5
            )

        elif parent_order.strategy == VWAP:

            return AdaptiveVWAPStrategy(

                total_qty=
                parent_order.quantity,

                target_participation=
                DEFAULT_PARTICIPATION,

                market_state=
                self.market_state
            )

        elif parent_order.strategy == POV:

            return POVStrategy(

                total_qty=
                parent_order.quantity
            )

        else:

            raise ValueError(

                f"Unsupported Strategy | "

                f"{parent_order.strategy}"
            )


    # ====================================
    # GET ACTIVE ORDERS
    # ====================================

    def get_active_orders(self):

        return {

            order_id:
            order.get_snapshot()

            for order_id, order

            in self.active_orders.items()
        }


    # ====================================
    # GET ORDER
    # ====================================

    def get_order(

        self,

        order_id
    ):

        return self.active_orders.get(
            order_id
        )


    # ====================================
    # GET POSITIONS
    # ====================================

    def get_positions(self):

        return (

            self.position_manager
            .get_all_positions()
        )


    # ====================================
    # GET PORTFOLIO SUMMARY
    # ====================================

    def get_portfolio_summary(self):

        return (

            self.position_manager
            .get_portfolio_summary()
        )


    # ====================================
    # STOP EXECUTION
    # ====================================

    def stop(self):

        self.status = HALTED

        self.logger.warning(
            "Execution Service Halted"
        )


    # ====================================
    # GET STATUS
    # ====================================

    def get_status(self):

        return {

            "status":
            self.status,

            "active_orders":
            len(self.active_orders),

            "positions":
            len(

                self.position_manager
                .get_all_positions()
            )
        }


    # ====================================
    # SHOW FILLS
    # ====================================

    def show_fills(self):

        self.fill_tracker.show_fills()


    # ====================================
    # SHOW EXECUTION LOGS
    # ====================================

    def show_logs(self):

        self.execution_logger.show_logs()


    # ====================================
    # SHOW POSITIONS
    # ====================================

    def show_positions(self):

        self.position_manager.show_positions()


    # ====================================
    # SHOW SUMMARY
    # ====================================

    def show_summary(self):

        print(

            "\n========== "
            "EXECUTION SERVICE "
            "==========\n"
        )

        print(

            f"Status: "
            f"{self.status}"
        )

        print(

            f"Active Orders: "
            f"{len(self.active_orders)}"
        )

        print(

            f"Positions: "
            f"{len(self.position_manager.get_all_positions())}"
        )

        print(

            "\n=======================================\n"
        )
