# ====================================
# fake_oms.py
# ====================================

import uuid
import random

from types import SimpleNamespace

from utils.logger import (
    SystemLogger
)

from utils.helpers import (
    get_current_time
)


class FakeOMS:


    # ====================================
    # INIT
    # ====================================

    def __init__(self):

        # ====================================
        # LOGGER
        # ====================================

        self.logger = (
            SystemLogger()
        )

        # ====================================
        # ORDER STORAGE
        # ====================================

        self.orders = []

        self.logger.info(
            "FakeOMS Initialized"
        )


    # ====================================
    # GET ACCOUNT
    # ====================================

    def get_account(self):

        return {

            "account_id":
            "SIMULATION",

            "buying_power":
            1000000,

            "equity":
            1000000,

            "currency":
            "USD"
        }


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
            # SUBMIT TIME
            # ====================================

            submit_time = (
                get_current_time()
            )

            # ====================================
            # FAKE ORDER ID
            # ====================================

            order_id = str(
                uuid.uuid4()
            )

            # ====================================
            # FAKE PRICE
            # ====================================

            simulated_price = round(

                random.uniform(
                    100,
                    300
                ),

                2
            )

            # ====================================
            # CREATE FAKE ORDER
            # ====================================

            order = SimpleNamespace(

                id=
                order_id,

                symbol=
                symbol,

                qty=
                qty,

                side=
                side,

                status=
                "filled",

                filled_avg_price=
                simulated_price
            )

            # ====================================
            # STORE ORDER
            # ====================================

            order_record = {

                "timestamp":
                submit_time,

                "order_id":
                order_id,

                "symbol":
                symbol,

                "qty":
                qty,

                "side":
                side,

                "status":
                "filled",

                "fill_price":
                simulated_price
            }

            self.orders.append(
                order_record
            )

            # ====================================
            # LOG
            # ====================================

            self.logger.info(

                f"Fake Order Submitted | "

                f"{symbol} | "

                f"{side} | "

                f"{qty} | "

                f"{simulated_price}"
            )

            return order

        except Exception as error:

            self.logger.error(

                f"FakeOMS Submission Failed | "

                f"{error}"
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

            for order in self.orders:

                if (

                    order["order_id"]
                    ==
                    order_id
                ):

                    return order

            return None

        except Exception as error:

            self.logger.error(

                f"Get Order Failed | "

                f"{error}"
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

            for order in self.orders:

                if (

                    order["order_id"]
                    ==
                    order_id
                ):

                    order["status"] = (
                        "cancelled"
                    )

                    self.logger.warning(

                        f"Order Cancelled | "

                        f"{order_id}"
                    )

                    return True

            return False

        except Exception as error:

            self.logger.error(

                f"Cancel Order Failed | "

                f"{error}"
            )

            return False


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

                "canceled",

                "cancelled"
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
    # GET ORDER COUNT
    # ====================================

    def get_order_count(self):

        return len(
            self.orders
        )


    # ====================================
    # SHOW SUMMARY
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

            "\n========== "
            "FAKE OMS SUMMARY "
            "==========\n"
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
    # ====================================
# GET POSITIONS
# ====================================

    def get_positions(self):

        positions = {}

        for order in self.orders:

            if order["status"] != "filled":

                continue

            symbol = order["symbol"]

            qty = order["qty"]

            side = order["side"]

            signed_qty = qty

            if side == "SELL":

                signed_qty = -qty

            if symbol not in positions:

                positions[symbol] = {

                    "quantity": 0
                }

            positions[symbol]["quantity"] += (
                signed_qty
            )

        return positions