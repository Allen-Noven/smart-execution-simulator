# ====================================
# parent_order.py
# ====================================

from uuid import uuid4

from utils.logger import (
    SystemLogger
)

from utils.helpers import (

    get_current_time,

    calculate_notional
)

from utils.constants import (

    BUY,

    SELL,

    RUNNING,

    COMPLETED,

    HALTED
)


class ParentOrder:

    def __init__(

        self,

        symbol,

        side,

        quantity,

        strategy,

        arrival_price=None

    ):

        # ====================================
        # LOGGER
        # ====================================

        self.logger = (
            SystemLogger()
        )

        # ====================================
        # ORDER ID
        # ====================================

        self.order_id = str(
            uuid4()
        )

        # ====================================
        # BASIC INFO
        # ====================================

        self.symbol = symbol

        self.side = side

        self.quantity = quantity
        
        self.total_qty = quantity


        self.strategy = strategy

        # ====================================
        # EXECUTION STATE
        # ====================================

        self.filled_quantity = 0

        self.remaining_quantity = (
            quantity
        )

        self.avg_fill_price = 0.0

        self.arrival_price = (
            arrival_price
        )

        # ====================================
        # STATUS
        # ====================================

        self.status = RUNNING

        # ====================================
        # TIMESTAMPS
        # ====================================

        self.created_at = (
            get_current_time()
        )

        self.completed_at = None

        # ====================================
        # EXECUTION METRICS
        # ====================================

        self.notional = 0.0

        self.realized_slippage = 0.0

        self.realized_bps = 0.0

        # ====================================
        # CHILD ORDERS
        # ====================================

        self.child_orders = []

        # ====================================
        # FILLS
        # ====================================

        self.fills = []

        # ====================================
        # VALIDATE
        # ====================================

        self.validate_order()

        # ====================================
        # LOG
        # ====================================

        self.logger.info(

            f"Parent Order Created | "

            f"{self.symbol} | "

            f"{self.side} | "

            f"Qty: {self.quantity}"
        )


    # ====================================
    # VALIDATE ORDER
    # ====================================

    def validate_order(self):

        if self.side not in [

            BUY,

            SELL

        ]:

            raise ValueError(

                "Invalid Order Side"
            )

        if self.quantity <= 0:

            raise ValueError(

                "Quantity Must Be Positive"
            )


    # ====================================
    # ADD CHILD ORDER
    # ====================================

    def add_child_order(

        self,

        child_order

    ):

        self.child_orders.append(
            child_order
        )

        self.logger.info(

            f"Child Order Added | "

            f"{child_order}"
        )


    # ====================================
    # ADD FILL
    # ====================================

    def add_fill(

        self,

        fill_qty,

        fill_price

    ):

        # ====================================
        # UPDATE FILLS
        # ====================================

        fill_data = {

            "timestamp":
            get_current_time(),

            "fill_qty":
            fill_qty,

            "fill_price":
            fill_price
        }

        self.fills.append(
            fill_data
        )

        # ====================================
        # UPDATE QUANTITY
        # ====================================

        self.filled_quantity += (
            fill_qty
        )

        self.remaining_quantity = max(

            0,

            self.quantity
            -
            self.filled_quantity
        )

        # ====================================
        # UPDATE AVG FILL PRICE
        # ====================================

        total_notional = sum(

            fill["fill_qty"]
            *
            fill["fill_price"]

            for fill in self.fills
        )

        total_qty = sum(

            fill["fill_qty"]

            for fill in self.fills
        )

        if total_qty > 0:

            self.avg_fill_price = round(

                total_notional
                /
                total_qty,

                4
            )

        # ====================================
        # UPDATE NOTIONAL
        # ====================================

        self.notional = (

            calculate_notional(

                self.filled_quantity,

                self.avg_fill_price
            )
        )

        # ====================================
        # COMPLETE ORDER
        # ====================================

        if (

            self.remaining_quantity
            <= 0

        ):

            self.complete_order()

        # ====================================
        # LOG
        # ====================================

        self.logger.info(

            f"Fill Added | "

            f"{self.symbol} | "

            f"Filled: {self.filled_quantity}/"

            f"{self.quantity}"
        )


    # ====================================
    # COMPLETE ORDER
    # ====================================

    def complete_order(self):

        self.status = COMPLETED

        self.completed_at = (
            get_current_time()
        )

        self.logger.info(

            f"Order Completed | "

            f"{self.symbol}"
        )


    # ====================================
    # HALT ORDER
    # ====================================

    def halt_order(

        self,

        reason

    ):

        self.status = HALTED

        self.logger.warning(

            f"Order Halted | "

            f"{reason}"
        )


    # ====================================
    # GET COMPLETION %
    # ====================================

    def get_completion_rate(self):

        if self.quantity == 0:

            return 0

        return round(

            (

                self.filled_quantity
                /
                self.quantity

            ) * 100,

            2
        )


    # ====================================
    # GET SNAPSHOT
    # ====================================

    def get_snapshot(self):

        return {

            "order_id":
            self.order_id,

            "symbol":
            self.symbol,

            "side":
            self.side,

            "strategy":
            self.strategy,

            "quantity":
            self.quantity,

            "filled_quantity":
            self.filled_quantity,

            "remaining_quantity":
            self.remaining_quantity,

            "completion_rate":
            self.get_completion_rate(),

            "avg_fill_price":
            self.avg_fill_price,

            "arrival_price":
            self.arrival_price,

            "status":
            self.status,

            "notional":
            self.notional,

            "created_at":
            str(self.created_at),

            "completed_at":
            str(self.completed_at)
            if self.completed_at
            else None
        }


    # ====================================
    # DISPLAY
    # ====================================

    def show(self):

        snapshot = (
            self.get_snapshot()
        )

        print(

            "\n========== PARENT ORDER ==========\n"
        )

        for key, value in snapshot.items():

            print(f"{key}: {value}")

        print(

            "\n==================================\n"
        )