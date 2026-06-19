# ====================================
# oms.py
# ====================================

from alpaca.trading.client import (
    TradingClient
)

from alpaca.trading.requests import (
    MarketOrderRequest
)

from alpaca.trading.enums import (

    OrderSide,

    TimeInForce
)

from utils.config import (

    API_KEY,

    SECRET_KEY,

    PAPER_TRADING
)

from utils.logger import (
    SystemLogger
)

from utils.helpers import (

    get_current_time,

    format_order_log
)

from utils.constants import (

    BUY,

    SELL
)


class OMS:

    def __init__(self):

        # ====================================
        # LOGGER
        # ====================================

        self.logger = (
            SystemLogger()
        )


        # ====================================
        # ALPACA TRADING CLIENT
        # ====================================

        self.trading_client = (

            TradingClient(

                API_KEY,

                SECRET_KEY,

                paper=PAPER_TRADING
            )
        )


        # ====================================
        # ORDER STORAGE
        # ====================================

        self.orders = []


    # ====================================
    # CONVERT SIDE
    # ====================================

    def convert_side(

        self,

        side

    ):

        if side == BUY:

            return OrderSide.BUY

        elif side == SELL:

            return OrderSide.SELL

        else:

            raise ValueError(

                f"Invalid side: {side}"
            )


    # ====================================
    # GET ACCOUNT
    # ====================================

    def get_account(self):

        return (
            self.trading_client.get_account()
        )


    # ====================================
    # SUBMIT MARKET ORDER
    # ====================================

    def submit_market_order(

        self,

        symbol,

        qty,

        side

    ):

        try:

            # ====================================
            # SIDE CONVERSION
            # ====================================

            alpaca_side = (
                self.convert_side(side)
            )


            # ====================================
            # CREATE ORDER REQUEST
            # ====================================

            market_order = (

                MarketOrderRequest(

                    symbol=symbol,

                    qty=qty,

                    side=alpaca_side,

                    time_in_force=
                    TimeInForce.DAY
                )
            )


            submit_time = (
                get_current_time()
            )


            # ====================================
            # SUBMIT ORDER
            # ====================================

            order = (

                self.trading_client.submit_order(

                    order_data=market_order
                )
            )


            # ====================================
            # STORE ORDER
            # ====================================

            order_record = {

                "timestamp":
                submit_time,

                "order_id":
                str(order.id),

                "symbol":
                symbol,

                "qty":
                qty,

                "side":
                side,

                "status":
                str(order.status)
            }

            self.orders.append(
                order_record
            )


            self.logger.info(

                f"Order Submitted | "

                f"{symbol} | "

                f"{side} | "

                f"{qty}"
            )


            return order


        except Exception as e:

            self.logger.error(

                f"Order Submission Failed | "
                f"{e}"
            )

            return None


    # ====================================
    # GET ORDER
    # ====================================

    def get_order(

        self,

        order_id

    ):

        try:

            return (

                self.trading_client
                .get_order_by_id(order_id)
            )

        except Exception as e:

            self.logger.error(

                f"Get Order Failed | "
                f"{e}"
            )

            return None


    # ====================================
    # CANCEL ORDER
    # ====================================

    def cancel_order(

        self,

        order_id

    ):

        try:

            self.trading_client.cancel_order_by_id(
                order_id
            )

            self.logger.warning(

                f"Order Cancelled | "
                f"{order_id}"
            )

        except Exception as e:

            self.logger.error(

                f"Cancel Order Failed | "
                f"{e}"
            )


    # ====================================
    # GET ALL ORDERS
    # ====================================

    def get_orders(self):

        return self.orders


    # ====================================
    # GET OPEN ORDERS
    # ====================================

    def get_open_orders(self):

        return [

            order

            for order in self.orders

            if order["status"]

            not in [

                "filled",

                "canceled"
            ]
        ]


    # ====================================
    # GET FILLED ORDERS
    # ====================================

    def get_filled_orders(self):

        return [

            order

            for order in self.orders

            if order["status"] == "filled"
        ]


    # ====================================
    # SHOW ORDER SUMMARY
    # ====================================

    def show_summary(self):

        total_orders = (
            len(self.orders)
        )

        filled_orders = (
            len(
                self.get_filled_orders()
            )
        )

        open_orders = (
            len(
                self.get_open_orders()
            )
        )

        print(

            "\n========== OMS SUMMARY ==========\n"
        )

        print(

            f"Total Orders: "
            f"{total_orders}"
        )

        print(

            f"Filled Orders: "
            f"{filled_orders}"
        )

        print(

            f"Open Orders: "
            f"{open_orders}"
        )

        print(

            "\n=================================\n"
        )