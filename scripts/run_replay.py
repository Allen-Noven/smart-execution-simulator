# ====================================
# run_replay.py
# ====================================

from utils.logger import (
    SystemLogger
)

from utils.config import (
    REPLAY_DATA_PATH
)

from portfolio.runtime_positions import (
    RuntimePositions
)

from portfolio.portfolio_state import (
    PortfolioState
)

from execution.execution_service import (
    ExecutionService
)

from data.replay import (
    ReplayMarket
)

from analytics.pnl_tracker import (
    PnLTracker
)

from analytics.trade_blotter import (
    TradeBlotter
)


# ====================================
# LOGGER
# ====================================

logger = SystemLogger()


# ====================================
# RUN REPLAY
# ====================================

def run_replay():

    logger.info(

        "Starting Replay Runtime..."
    )


    # ====================================
    # INITIALIZE RUNTIME POSITIONS
    # ====================================

    logger.info(

        "Initializing Runtime Positions..."
    )

    runtime_positions = (
        RuntimePositions()
    )

    portfolio_state = (
        PortfolioState(
            runtime_positions
        )
    )


    # ====================================
    # INITIALIZE ANALYTICS
    # ====================================

    logger.info(

        "Initializing Analytics..."
    )

    pnl_tracker = (
        PnLTracker()
    )

    trade_blotter = (
        TradeBlotter()
    )


    # ====================================
    # INITIALIZE REPLAY MARKET
    # ====================================

    logger.info(

        "Loading Replay Data..."
    )

    replay_market = (

        ReplayMarket(
            REPLAY_DATA_PATH
        )
    )


    # ====================================
    # INITIALIZE EXECUTION SERVICE
    # ====================================

    logger.info(

        "Initializing Execution Service..."
    )

    execution_service = (
        ExecutionService()
    )


    # ====================================
    # START REPLAY LOOP
    # ====================================

    logger.info(

        "Replay Runtime Started"
    )

    for market_event in (

        replay_market.stream_market()
    ):

        # ====================================
        # PROCESS MARKET EVENT
        # ====================================

        execution_service.process_market_event(

            market_event
        )


        # ====================================
        # UPDATE PORTFOLIO STATE
        # ====================================

        portfolio_state.get_portfolio_summary()


    # ====================================
    # END OF REPLAY
    # ====================================

    logger.info(

        "Replay Completed"
    )


    # ====================================
    # FINAL REPORTING
    # ====================================

    runtime_positions.show_positions()

    portfolio_state.show_portfolio_summary()

    trade_blotter.generate_report()


# ====================================
# MAIN
# ====================================

if __name__ == "__main__":

    run_replay()