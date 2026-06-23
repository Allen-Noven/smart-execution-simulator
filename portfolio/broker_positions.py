# ====================================
# broker_position_service.py
# ====================================

from alpaca.trading.client import (
    TradingClient
)

from utils.logger import (
    SystemLogger
)

from utils.helpers import (

    format_price,

    get_current_timestamp
)

from utils.config import (

    API_KEY,

    SECRET_KEY,

    PAPER_TRADING
)

from utils.constants import (

    ALPACA,

    SYSTEM_RUNNING,

    SYSTEM_ERROR
)


class BrokerPositionService:


    # ====================================
    # INIT
    # ====================================

    def __init__(self):

        self.logger = (
            SystemLogger()
        )

        self.broker_name = (
            ALPACA
        )

        self.status = (
            SYSTEM_RUNNING
        )

        self.last_sync_time = None

        self.positions = {}

        self.trading_client = (

            TradingClient(

                API_KEY,

                SECRET_KEY,

                paper=PAPER_TRADING
            )
        )

        self.logger.info(

            "Broker Position Service Initialized"
        )


    # ====================================
    # FETCH BROKER POSITIONS
    # ====================================

    def fetch_positions(self):

        try:

            broker_positions = (

                self.trading_client
                .get_all_positions()
            )

            formatted_positions = {}


            # ====================================
            # FORMAT POSITIONS
            # ====================================

            for position in broker_positions:

                symbol = (
                    position.symbol
                )

                qty = float(
                    position.qty
                )

                avg_price = float(

                    position.avg_entry_price
                )

                market_value = float(
                    position.market_value
                )

                unrealized_pl = float(

                    position.unrealized_pl
                )

                formatted_positions[
                    symbol
                ] = {

                    "qty":
                    qty,

                    "avg_price":
                    format_price(
                        avg_price
                    ),

                    "market_value":
                    format_price(
                        market_value
                    ),

                    "unrealized_pl":
                    format_price(
                        unrealized_pl
                    )
                }


            # ====================================
            # UPDATE CACHE
            # ====================================

            self.positions = (
                formatted_positions
            )

            self.last_sync_time = (
                get_current_timestamp()
            )

            self.status = (
                SYSTEM_RUNNING
            )

            self.logger.info(

                f"Broker Positions Synced | "

                f"{len(self.positions)} "

                f"positions loaded"
            )

            return self.positions


        except Exception as error:

            self.status = (
                SYSTEM_ERROR
            )

            self.logger.error(

                f"Broker Position Sync Failed | "

                f"{error}"
            )

            return {}


    # ====================================
    # GET POSITION
    # ====================================

    def get_position(

        self,

        symbol
    ):

        return self.positions.get(

            symbol,

            None
        )


    # ====================================
    # GET ALL POSITIONS
    # ====================================

    def get_all_positions(self):

        return self.positions


    # ====================================
    # GET TOTAL MARKET VALUE
    # ====================================

    def get_total_market_value(self):

        total_market_value = 0

        for symbol in self.positions:

            total_market_value += abs(

                self.positions[symbol][
                    "market_value"
                ]
            )

        return format_price(
            total_market_value
        )


    # ====================================
    # GET TOTAL UNREALIZED PNL
    # ====================================

    def get_total_unrealized_pnl(self):

        total_unrealized_pnl = 0

        for symbol in self.positions:

            total_unrealized_pnl += (

                self.positions[symbol][
                    "unrealized_pl"
                ]
            )

        return format_price(
            total_unrealized_pnl
        )


    # ====================================
    # GET LAST SYNC TIME
    # ====================================

    def get_last_sync_time(self):

        return self.last_sync_time


    # ====================================
    # GET SERVICE STATUS
    # ====================================

    def get_status(self):

        return self.status


    # ====================================
    # SHOW POSITIONS
    # ====================================

    def show_positions(self):

        print(

            "\n========== "
            "BROKER POSITIONS "
            "==========\n"
        )

        for symbol, position in (

            self.positions.items()
        ):

            print(

                f"{symbol} | "

                f"Qty: {position['qty']} | "

                f"Avg Price: "
                f"{position['avg_price']} | "

                f"Market Value: "
                f"{position['market_value']} | "

                f"Unrealized PnL: "
                f"{position['unrealized_pl']}"
            )

        print(

            "\nTotal Market Value: "

            f"{self.get_total_market_value()}"
        )

        print(

            f"Total Unrealized PnL: "

            f"{self.get_total_unrealized_pnl()}"
        )

        print(

            f"Last Sync: "

            f"{self.last_sync_time}"
        )

        print(

            "\n==============================="
            "===================\n"
        )


    # ====================================
    # REFRESH POSITIONS
    # ====================================

    def refresh(self):

        self.logger.info(

            "Refreshing broker positions..."
        )

        return self.fetch_positions()
