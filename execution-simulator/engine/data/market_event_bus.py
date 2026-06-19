# ====================================
# market_event_bus.py
# ====================================

from collections import defaultdict

from utils.logger import (
    SystemLogger
)


class MarketEventBus:

    def __init__(self):

        self.logger = (
            SystemLogger()
        )

        self.subscribers = (
            defaultdict(list)
        )


    # ====================================
    # SUBSCRIBE
    # ====================================

    def subscribe(

        self,

        event_type,

        callback

    ):

        self.subscribers[
            event_type
        ].append(callback)

        self.logger.info(

            f"Subscribed | "
            f"{event_type}"
        )


    # ====================================
    # PUBLISH EVENT
    # ====================================

    def publish(

        self,

        event_type,

        data

    ):

        callbacks = (

            self.subscribers
            .get(event_type, [])
        )

        self.logger.info(

            f"Publishing Event | "
            f"{event_type}"
        )

        for callback in callbacks:

            try:

                callback(data)

            except Exception as e:

                self.logger.error(

                    f"Event Error | {e}"
                )