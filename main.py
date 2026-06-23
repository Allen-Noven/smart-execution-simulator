# ====================================
# main.py
# ====================================

from runtime.runtime_bootstrap import (
    RuntimeBootstrap
)

from utils.logger import (
    SystemLogger
)


# ====================================
# LOGGER
# ====================================

logger = (
    SystemLogger()
)


# ====================================
# MAIN
# ====================================

def main():

    bootstrap = None

    try:

        logger.info(
            "Launching Trading Runtime"
        )

        # ====================================
        # INITIALIZE RUNTIME
        # ====================================

        bootstrap = (
            RuntimeBootstrap()
        )

        # ====================================
        # START RUNTIME
        # ====================================

        bootstrap.bootstrap()

        logger.info(
            "Trading Runtime Started"
        )

        # ====================================
        # START RECONCILIATION
        # ====================================

        if hasattr(

            bootstrap,

            "reconciliation_engine"
        ):

            bootstrap.reconciliation_engine.reconcile_all()

        logger.info(
            "Runtime Healthy"
        )

    except KeyboardInterrupt:

        logger.warning(
            "System Interrupted"
        )

    except Exception as error:

        logger.error(

            f"Fatal Runtime Error | "

            f"{error}"
        )

    finally:

        # ====================================
        # CLEAN SHUTDOWN
        # ====================================

        try:

            if bootstrap:

                bootstrap.shutdown()

                logger.warning(
                    "Runtime Shutdown Complete"
                )

        except Exception as error:

            logger.error(

                f"Shutdown Failed | "

                f"{error}"
            )


# ====================================
# ENTRYPOINT
# ====================================

if __name__ == "__main__":

    main()