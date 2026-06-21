# ====================================
# main.py
# ====================================

from core.market_state import (
    MarketState
)

from core.system_state import (
    SystemState
)

from core.global_state import (
    system_state
)

from core.redis_state import (
    RedisState
)

from core.execution_engine import (
    start_execution_engine
)

from data.market_event_bus import (
    MarketEventBus
)

from data.replay import (
    MarketReplay
)

from risk.liquidity_monitor import (
    LiquidityMonitor
)

from risk.kill_switch import (
    KillSwitch
)

from risk.ai_risk_classifier import (
    AIRiskClassifier
)

from notifications.email_service import (
    EmailService
)

from utils.constants import (

    MARKET_UPDATE_EVENT,

    AI_RISK_EVENT
)

from utils.logger import (
    SystemLogger
)

from utils.config import (

    DEFAULT_SYMBOL,

    DATA_MODE
)

from data.real_time_data_loader import (
    RealTimeDataLoader
)

from data.fake_market_generator import (
    FakeMarketGenerator
)


# ====================================
# LOGGER
# ====================================

logger = (
    SystemLogger()
)


# ====================================
# REDIS STATE
# ====================================

redis_state = RedisState()


# ====================================
# INITIALIZE ALERTS
# ====================================

redis_state.set_alerts([])


# ====================================
# GLOBAL SYSTEM STATE
# ====================================

market_state = (
    system_state.market_state
)


# ====================================
# EVENT BUS
# ====================================

event_bus = (
    MarketEventBus()
)


# ====================================
# EMAIL SERVICE
# ====================================

email_service = (
    EmailService()
)


# ====================================
# RISK COMPONENTS
# ====================================

liquidity_monitor = (

    LiquidityMonitor(

        market_state=
        market_state
    )
)

kill_switch = (

    KillSwitch(

        system_state=
        system_state,

        event_bus=
        event_bus
    )
)


# ====================================
# AI RISK ENGINE
# ====================================

ai_risk_classifier = (

    AIRiskClassifier(

        event_bus=
        event_bus
    )
)


# ====================================
# EVENT SUBSCRIPTIONS
# ====================================

event_bus.subscribe(

    MARKET_UPDATE_EVENT,

    liquidity_monitor.on_market_update
)

event_bus.subscribe(

    AI_RISK_EVENT,

    kill_switch.on_ai_risk
)


# ====================================
# MARKET REPLAY
# ====================================

replay = (

    MarketReplay(

        data_path=
        "data/nvda_data.csv",

        market_state=
        market_state,

        event_bus=
        event_bus
    )
)


# ====================================
# REAL-TIME DATA LOADER
# ====================================

real_time_data_loader = (

    RealTimeDataLoader(

        market_state=
        market_state
    )
)


# ====================================
# FAKE MARKET GENERATOR
# ====================================

fake_market_generator = (

    FakeMarketGenerator(

        market_state=
        market_state,
        event_bus=
        event_bus
    )
)


# ====================================
# STARTUP LOG
# ====================================

logger.info(
    "===================================="
)

logger.info(
    "Starting Smart Execution Platform"
)

logger.info(
    f"Symbol: {DEFAULT_SYMBOL}"
)

logger.info(
    "===================================="
)


# ====================================
# START EXECUTION ENGINE
# ====================================

logger.info(
    "Starting Execution Engine"
)

start_execution_engine()


# ====================================
# START MARKET DATA ENGINE
# ====================================

try:

    if DATA_MODE == "replay":

        logger.info(
            "Running Replay Mode"
        )

        replay.run()

    elif DATA_MODE == "live":

        logger.info(
            "Running Live Mode"
        )

        real_time_data_loader.start()

    elif DATA_MODE == "fake":

        logger.info(
            "Running Fake Mode"
        )

        fake_market_generator.start()

    else:

        raise ValueError(
            "Invalid Data Mode"
        )

except KeyboardInterrupt:

    logger.warning(
        "System Interrupted"
    )

except Exception as e:

    logger.error(

        f"System Failure | "
        f"{e}"
    )

    # ====================================
    # UPDATE REDIS STATUS
    # ====================================

    redis_state.set_execution_status(

        {

            "status":
            "FAILED",

            "halted":
            True,

            "reason":
            str(e)
        }
    )

    redis_state.set_alerts(

        [

            f"System Failure | {e}"
        ]
    )

    # ====================================
    # EMAIL ALERT
    # ====================================

    try:

        email_service.send_alert(

            subject=
            "System Failure",

            body=
            str(e),

            severity=
            "CRITICAL"
        )

    except Exception as email_error:

        logger.error(

            f"Email Failure | "
            f"{email_error}"
        )