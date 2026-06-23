# ====================================
# runtime_bootstrap.py
# ====================================
from storage.order_repository import (
    OrderRepository
)

from storage.position_repository import (
    PositionRepository
)
from runtime.runtime_context import (

    market_state,

    event_bus,

    execution_service,

    execution_worker
)

from utils.logger import (
    SystemLogger
)

from utils.runtime_mode import (
    RUNTIME_MODE
)


class RuntimeBootstrap:


    # ====================================
    # INIT
    # ====================================

    def __init__(self):

        self.logger = (
            SystemLogger()
        )
        # ====================================
        # ORDER REPOSITORY
        # ====================================

        self.order_repository = (
            OrderRepository()
        )

        # ====================================
        # POSITION REPOSITORY
        # ====================================

        self.position_repository = (
            PositionRepository()
        )


    # ====================================
    # BOOTSTRAP
    # ====================================

    def bootstrap(self):

        self.logger.info(

            f"Bootstrapping Runtime | "

            f"Mode={RUNTIME_MODE}"
        )

        # ====================================
        # START WORKER
        # ====================================

        self.start_execution_worker()



            # ====================================
    # RECOVER STATE
    # ====================================

    def recover_runtime_state(self):

        try:

            self.logger.info(
                "Recovering Runtime State"
            )

            # ====================================
            # LOAD POSITIONS
            # ====================================

            positions = (

                self.position_repository
                .load_positions()
            )

            # ====================================
            # LOAD ACTIVE ORDERS
            # ====================================

            active_orders = (

                self.order_repository
                .load_active_orders()
            )

        # ====================================
        # LOG POSITIONS
        # ====================================

        self.logger.info(

            f"Recovered Positions | "

            f"{len(positions)}"
        )

        # ====================================
        # LOG ACTIVE ORDERS
        # ====================================

        self.logger.info(

            f"Recovered Active Orders | "

            f"{len(active_orders)}"
        )

        # ====================================
        # FUTURE:
        # rebuild runtime objects
        # reconcile broker
        # recover fills
        # ====================================

    except Exception as error:

        self.logger.error(

            f"Recovery Failed | "

            f"{error}"
        )

        self.logger.info(
            "Runtime Bootstrap Complete"
        )


    # ====================================
    # START EXECUTION WORKER
    # ====================================

    def start_execution_worker(self):

        try:

            execution_worker.start()

            self.logger.info(
                "Execution Worker Started"
            )

        except Exception as error:

            self.logger.error(

                f"Execution Worker Failed | "

                f"{error}"
            )


    # ====================================
    # RECOVER STATE
    # ====================================

    def recover_runtime_state(self):

        try:

            self.logger.info(
                "Recovering Runtime State"
            )

            # future:
            # recover positions
            # recover orders
            # reconcile broker

        except Exception as error:

            self.logger.error(

                f"Recovery Failed | "

                f"{error}"
            )


    # ====================================
    # SHUTDOWN
    # ====================================

    def shutdown(self):

        self.logger.warning(
            "Runtime Shutdown Started"
        )

        try:

            execution_worker.stop()

        except Exception as error:

            self.logger.error(

                f"Worker Shutdown Failed | "

                f"{error}"
            )

        self.logger.warning(
            "Runtime Shutdown Complete"
        )
