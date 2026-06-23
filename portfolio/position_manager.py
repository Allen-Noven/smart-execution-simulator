# ====================================
# position_manager.py
# ====================================

from utils.logger import (
    SystemLogger
)

from utils.helpers import (

    calculate_notional,

    format_price
)


class PositionManager:


    # ====================================
    # INIT
    # ====================================

    def __init__(self):

        self.logger = (
            SystemLogger()
        )

        # ====================================
        # POSITION BOOK
        # ====================================

        self.positions = {}

        # ====================================
        # PORTFOLIO METRICS
        # ====================================

        self.total_realized_pnl = 0

        self.total_unrealized_pnl = 0

        self.total_exposure = 0

        self.logger.info(
            "Position Manager Initialized"
        )


    # ====================================
    # CREATE EMPTY POSITION
    # ====================================

    def create_position(

        self,

        symbol
    ):

        self.positions[symbol] = {

            "symbol":
            symbol,

            "qty":
            0,

            "avg_price":
            0,

            "market_price":
            0,

            "market_value":
            0,

            "realized_pnl":
            0,

            "unrealized_pnl":
            0,

            "total_bought":
            0,

            "total_sold":
            0
        }


    # ====================================
    # UPDATE POSITION
    # ====================================

    def update_position(

        self,

        symbol,

        side,

        qty,

        fill_price,

        market_price=None
    ):

        # ====================================
        # CREATE POSITION
        # ====================================

        if symbol not in self.positions:

            self.create_position(
                symbol
            )

        position = (
            self.positions[symbol]
        )

        # ====================================
        # CURRENT STATE
        # ====================================

        current_qty = (
            position["qty"]
        )

        current_avg_price = (
            position["avg_price"]
        )

        realized_pnl = (
            position["realized_pnl"]
        )

        # ====================================
        # DEFAULT MARKET PRICE
        # ====================================

        if market_price is None:

            market_price = fill_price

        # ====================================
        # BUY
        # ====================================

        if side == "BUY":

            # ====================================
            # SHORT COVER
            # ====================================

            if current_qty < 0:

                closing_qty = min(

                    abs(current_qty),

                    qty
                )

                pnl = (

                    current_avg_price
                    -
                    fill_price

                ) * closing_qty

                realized_pnl += pnl

                remaining_qty = (
                    qty - closing_qty
                )

                new_qty = (
                    current_qty + qty
                )

                # ====================================
                # POSITION FLIP
                # ====================================

                if new_qty > 0:

                    new_avg_price = (
                        fill_price
                    )

                elif new_qty == 0:

                    new_avg_price = 0

                else:

                    new_avg_price = (
                        current_avg_price
                    )

            # ====================================
            # LONG ADD
            # ====================================

            else:

                new_qty = (
                    current_qty + qty
                )

                total_cost = (

                    (
                        current_qty
                        *
                        current_avg_price
                    )

                    +

                    (
                        qty
                        *
                        fill_price
                    )
                )

                if new_qty == 0:

                    new_avg_price = 0

                else:

                    new_avg_price = (

                        total_cost
                        /
                        new_qty
                    )

            position[
                "total_bought"
            ] += qty

        # ====================================
        # SELL
        # ====================================

        else:

            # ====================================
            # LONG REDUCE
            # ====================================

            if current_qty > 0:

                closing_qty = min(

                    current_qty,

                    qty
                )

                pnl = (

                    fill_price
                    -
                    current_avg_price

                ) * closing_qty

                realized_pnl += pnl

                new_qty = (
                    current_qty - qty
                )

                # ====================================
                # POSITION FLIP
                # ====================================

                if new_qty < 0:

                    new_avg_price = (
                        fill_price
                    )

                elif new_qty == 0:

                    new_avg_price = 0

                else:

                    new_avg_price = (
                        current_avg_price
                    )

            # ====================================
            # SHORT ADD
            # ====================================

            else:

                new_qty = (
                    current_qty - qty
                )

                total_cost = (

                    (
                        abs(current_qty)
                        *
                        current_avg_price
                    )

                    +

                    (
                        qty
                        *
                        fill_price
                    )
                )

                if abs(new_qty) == 0:

                    new_avg_price = 0

                else:

                    new_avg_price = (

                        total_cost
                        /
                        abs(new_qty)
                    )

            position[
                "total_sold"
            ] += qty

        # ====================================
        # MARKET VALUE
        # ====================================

        market_value = (
            calculate_notional(

                new_qty,

                market_price
            )
        )

        # ====================================
        # UNREALIZED PNL
        # ====================================

        if new_qty > 0:

            unrealized_pnl = (

                market_price
                -
                new_avg_price

            ) * new_qty

        elif new_qty < 0:

            unrealized_pnl = (

                new_avg_price
                -
                market_price

            ) * abs(new_qty)

        else:

            unrealized_pnl = 0

        # ====================================
        # UPDATE POSITION
        # ====================================

        self.positions[symbol] = {

            "symbol":
            symbol,

            "qty":
            new_qty,

            "avg_price":
            format_price(
                new_avg_price
            ),

            "market_price":
            format_price(
                market_price
            ),

            "market_value":
            format_price(
                market_value
            ),

            "realized_pnl":
            format_price(
                realized_pnl
            ),

            "unrealized_pnl":
            format_price(
                unrealized_pnl
            ),

            "total_bought":
            position["total_bought"],

            "total_sold":
            position["total_sold"]
        }

        # ====================================
        # UPDATE PORTFOLIO METRICS
        # ====================================

        self.recalculate_portfolio()

        # ====================================
        # LOG
        # ====================================

        self.logger.info(

            f"Position Updated | "

            f"{symbol} | "

            f"Qty: {new_qty} | "

            f"Avg: {new_avg_price} | "

            f"Realized: {realized_pnl} | "

            f"Unrealized: {unrealized_pnl}"
        )


    # ====================================
    # RECALCULATE PORTFOLIO
    # ====================================

    def recalculate_portfolio(self):

        total_realized = 0

        total_unrealized = 0

        total_exposure = 0

        for position in (

            self.positions.values()
        ):

            total_realized += (

                position[
                    "realized_pnl"
                ]
            )

            total_unrealized += (

                position[
                    "unrealized_pnl"
                ]
            )

            total_exposure += abs(

                position[
                    "market_value"
                ]
            )

        self.total_realized_pnl = (
            format_price(
                total_realized
            )
        )

        self.total_unrealized_pnl = (
            format_price(
                total_unrealized
            )
        )

        self.total_exposure = (
            format_price(
                total_exposure
            )
        )


    # ====================================
    # MARK TO MARKET
    # ====================================

    def mark_to_market(

        self,

        symbol,

        market_price
    ):

        if symbol not in self.positions:

            return

        position = (
            self.positions[symbol]
        )

        qty = (
            position["qty"]
        )

        avg_price = (
            position["avg_price"]
        )

        # ====================================
        # MARKET VALUE
        # ====================================

        market_value = (
            calculate_notional(

                qty,

                market_price
            )
        )

        # ====================================
        # UNREALIZED PNL
        # ====================================

        if qty > 0:

            unrealized_pnl = (

                market_price
                -
                avg_price

            ) * qty

        elif qty < 0:

            unrealized_pnl = (

                avg_price
                -
                market_price

            ) * abs(qty)

        else:

            unrealized_pnl = 0

        # ====================================
        # UPDATE POSITION
        # ====================================

        position[
            "market_price"
        ] = format_price(
            market_price
        )

        position[
            "market_value"
        ] = format_price(
            market_value
        )

        position[
            "unrealized_pnl"
        ] = format_price(
            unrealized_pnl
        )

        # ====================================
        # RECALCULATE PORTFOLIO
        # ====================================

        self.recalculate_portfolio()


    # ====================================
    # GET POSITION
    # ====================================

    def get_position(

        self,

        symbol
    ):

        return self.positions.get(
            symbol
        )


    # ====================================
    # GET ALL POSITIONS
    # ====================================

    def get_all_positions(self):

        return self.positions


    # ====================================
    # GET PORTFOLIO SUMMARY
    # ====================================

    def get_portfolio_summary(self):

        return {

            "total_realized_pnl":
            self.total_realized_pnl,

            "total_unrealized_pnl":
            self.total_unrealized_pnl,

            "total_exposure":
            self.total_exposure,

            "position_count":
            len(self.positions)
        }


    # ====================================
    # RESET POSITIONS
    # ====================================

    def reset_positions(self):

        self.positions = {}

        self.total_realized_pnl = 0

        self.total_unrealized_pnl = 0

        self.total_exposure = 0

        self.logger.warning(
            "All Positions Reset"
        )


    # ====================================
    # SHOW POSITIONS
    # ====================================

    def show_positions(self):

        print(

            "\n========== "
            "PORTFOLIO POSITIONS "
            "==========\n"
        )

        for symbol, position in (

            self.positions.items()
        ):

            print(

                f"{symbol} | "

                f"Qty: {position['qty']} | "

                f"Avg: {position['avg_price']} | "

                f"Mkt: {position['market_price']} | "

                f"UPnL: {position['unrealized_pnl']} | "

                f"RPnL: {position['realized_pnl']}"
            )

        print(

            "\n========== "
            "PORTFOLIO SUMMARY "
            "==========\n"
        )

        print(

            f"Total Realized PnL: "
            f"{self.total_realized_pnl}"
        )

        print(

            f"Total Unrealized PnL: "
            f"{self.total_unrealized_pnl}"
        )

        print(

            f"Total Exposure: "
            f"{self.total_exposure}"
        )

        print(

            "\n====================================\n"
        )