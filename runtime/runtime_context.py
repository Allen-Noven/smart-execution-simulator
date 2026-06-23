# ====================================
# runtime_context.py
# ====================================

from utils.logger import (
    SystemLogger
)

from utils.runtime_mode import (

    RUNTIME_MODE,

    SIMULATION,

    LIVE,

    PAPER
)

from core.market_state import (
    MarketState
)

from core.redis_state import (
    RedisState
)

from data.market_event_bus import (
    MarketEventBus
)

from execution.order_queue import (
    OrderQueue
)

from execution.execution_service import (
    ExecutionService
)

from execution.execution_worker import (
    ExecutionWorker
)

from portfolio.position_manager import (
    PositionManager
)

from execution.oms.fake_oms import (
    FakeOMS
)

from execution.oms import (
    OMS
)


# ====================================
# LOGGER
# ====================================

logger = (
    SystemLogger()
)


# ====================================
# EVENT BUS
# ====================================

event_bus = (
    MarketEventBus()
)

logger.info(
    "Runtime EventBus Initialized"
)


# ====================================
# MARKET STATE
# ====================================

market_state = (
    MarketState()
)

logger.info(
    "Runtime MarketState Initialized"
)


# ====================================
# REDIS STATE
# ====================================

redis_state = (
    RedisState()
)

logger.info(
    "Runtime RedisState Initialized"
)


# ====================================
# OMS RUNTIME SELECTION
# ====================================

if RUNTIME_MODE == SIMULATION:

    oms = FakeOMS()

    logger.warning(
        "Runtime Using FakeOMS"
    )

else:

    oms = OMS()

    logger.warning(
        "Runtime Using Live OMS"
    )


# ====================================
# POSITION MANAGER
# ====================================

position_manager = (
    PositionManager()
)

logger.info(
    "Runtime PositionManager Initialized"
)


# ====================================
# EXECUTION SERVICE
# ====================================

execution_service = (

    ExecutionService(

        market_state=
        market_state,

        event_bus=
        event_bus,

        oms=
        oms
    )
)

# ====================================
# INJECT POSITION MANAGER
# ====================================

execution_service.position_manager = (
    position_manager
)

logger.info(
    "Runtime ExecutionService Initialized"
)


# ====================================
# ORDER QUEUE
# ====================================

order_queue = (
    OrderQueue()
)

logger.info(
    "Runtime OrderQueue Initialized"
)


# ====================================
# EXECUTION WORKER
# ====================================

execution_worker = (

    ExecutionWorker(

        order_queue=
        order_queue,

        execution_service=
        execution_service
    )
)

logger.info(
    "Runtime ExecutionWorker Initialized"
)


# ====================================
# RUNTIME STATUS
# ====================================

runtime_status = {

    "initialized":
    True,

    "worker_running":
    False
}


# ====================================
# START WORKER
# ====================================

def start_worker():

    import threading

    global runtime_status

    if execution_worker.is_running():

        logger.warning(
            "Execution Worker Already Running"
        )

        return

    worker_thread = threading.Thread(

        target=
        execution_worker.start,

        daemon=True
    )

    worker_thread.start()

    runtime_status[
        "worker_running"
    ] = True

    logger.info(
        "Runtime Worker Started"
    )


# ====================================
# STOP WORKER
# ====================================

def stop_worker():

    global runtime_status

    execution_worker.stop()

    runtime_status[
        "worker_running"
    ] = False

    logger.warning(
        "Runtime Worker Stopped"
    )


# ====================================
# GET RUNTIME STATUS
# ====================================

def get_runtime_status():

    return {

        "runtime_mode":
        RUNTIME_MODE,

        "initialized":
        runtime_status["initialized"],

        "worker_running":
        runtime_status["worker_running"],

        "queue_size":
        order_queue.size(),

        "worker_status":
        execution_worker.status,

        "positions":
        position_manager.get_all_positions(),

        "portfolio_summary":
        position_manager.get_portfolio_summary()
    }


# ====================================
# SHOW RUNTIME STATUS
# ====================================

def show_runtime_status():

    status = (
        get_runtime_status()
    )

    print(

        "\n========== RUNTIME STATUS ==========\n"
    )

    for key, value in status.items():

        print(f"{key}: {value}")

    print(

        "\n====================================\n"
    )