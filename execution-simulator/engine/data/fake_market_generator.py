# ====================================
# fake_market_generator.py
# ====================================

import time
import random

from utils.logger import (
    SystemLogger
)

from utils.constants import (
    MARKET_UPDATE_EVENT
)

from utils.config import (
    EXECUTION_INTERVAL
)


class FakeMarketGenerator:

    def __init__(

        self,

        market_state,

        event_bus,

        start_price=172.0,

        volatility=0.5

    ):

        # ====================================
        # LOGGER
        # ====================================

        self.logger = (
            SystemLogger()
        )

        # ====================================
        # SHARED COMPONENTS
        # ====================================

        self.market_state = (
            market_state
        )

        self.event_bus = (
            event_bus
        )

        # ====================================
        # MARKET PARAMETERS
        # ====================================

        self.price = (
            start_price
        )

        self.volatility = (
            volatility
        )

        self.running = False


    # ====================================
    # START GENERATOR
    # ====================================

    def start(self):

        self.logger.info(
            "Starting Fake Market Generator"
        )

        self.running = True

        while self.running:

            # ====================================
            # RANDOM WALK
            # ====================================

            self.price += random.uniform(

                -self.volatility,

                self.volatility
            )

            self.price = round(
                self.price,
                2
            )

            # ====================================
            # FAKE SPREAD
            # ====================================

            spread = round(

                random.uniform(
                    0.01,
                    0.08
                ),

                2
            )

            bid_price = round(
                self.price - spread / 2,
                2
            )

            ask_price = round(
                self.price + spread / 2,
                2
            )

            # ====================================
            # FAKE VOLUME
            # ====================================

            volume = random.randint(
                1000,
                10000
            )

            # ====================================
            # FAKE LIQUIDITY
            # ====================================

            liquidity_score = random.randint(
                20,
                100
            )

            # ====================================
            # FAKE VOLATILITY
            # ====================================

            market_volatility = round(

                random.uniform(
                    0.1,
                    3.0
                ),

                2
            )

            # ====================================
            # UPDATE MARKET STATE
            # ====================================

            self.market_state.update(

                price=
                self.price,

                volume=
                volume,

                bid_price=
                bid_price,

                ask_price=
                ask_price,

                volatility=
                market_volatility,

                liquidity_score=
                liquidity_score
            )

            # ====================================
            # PUBLISH EVENT
            # ====================================

            self.event_bus.publish(

                MARKET_UPDATE_EVENT,

                self.market_state
            )

            # ====================================
            # LOG
            # ====================================

            self.logger.info(

                f"Fake Tick | "

                f"Price: {self.price} | "

                f"Spread: {spread} | "

                f"Liquidity: {liquidity_score}"
            )

            # ====================================
            # WAIT
            # ====================================

            time.sleep(
                EXECUTION_INTERVAL
            )


    # ====================================
    # STOP GENERATOR
    # ====================================

    def stop(self):

        self.running = False