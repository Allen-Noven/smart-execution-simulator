# ====================================
# main.py
# ====================================

from core.market_state import (
    MarketState
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

from utils.constants import (

    MARKET_UPDATE_EVENT,

    AI_RISK_EVENT
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
# CREATE CORE STATE
# ====================================

market_state = (
    MarketState()
)

# ====================================
# CREATE EVENT BUS
# ====================================

event_bus = (
    MarketEventBus()
)

# ====================================
# CREATE RISK COMPONENTS
# ====================================

liquidity_monitor = (

    LiquidityMonitor(
        market_state
    )
)

kill_switch = (

    KillSwitch(

        system_state=None,

        event_bus=event_bus
    )
)

# ====================================
# CREATE AI ENGINE
# ====================================

ai_risk_classifier = (

    AIRiskClassifier(
        event_bus=event_bus
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
# CREATE REPLAY ENGINE
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
# START SYSTEM
# ====================================

logger.info(
    "Starting Smart Execution Platform"
)

# ====================================
# START REPLAY
# ====================================

replay.run()