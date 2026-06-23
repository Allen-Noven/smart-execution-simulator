# ====================================
# constants.py
# ====================================


# ====================================
# ORDER SIDES
# ====================================

BUY = "BUY"

SELL = "SELL"


# ====================================
# EXECUTION STRATEGIES
# ====================================

TWAP = "TWAP"

VWAP = "VWAP"

POV = "POV"


# ====================================
# DATA MODES
# ====================================

LIVE = "LIVE"

REPLAY = "REPLAY"

FAKE = "FAKE"


# ====================================
# ENVIRONMENTS
# ====================================

DEVELOPMENT = "DEVELOPMENT"

PAPER = "PAPER"

PRODUCTION = "PRODUCTION"


# ====================================
# ORDER STATUS
# ====================================

PENDING = "PENDING"

RUNNING = "RUNNING"

PARTIALLY_FILLED = (
    "PARTIALLY_FILLED"
)

COMPLETED = "COMPLETED"

CANCELLED = "CANCELLED"

REJECTED = "REJECTED"

FAILED = "FAILED"

HALTED = "HALTED"


# ====================================
# SYSTEM STATUS
# ====================================

SYSTEM_RUNNING = (
    "SYSTEM_RUNNING"
)

SYSTEM_HALTED = (
    "SYSTEM_HALTED"
)

SYSTEM_ERROR = (
    "SYSTEM_ERROR"
)


# ====================================
# MARKET SESSIONS
# ====================================

PREMARKET = "PREMARKET"

REGULAR = "REGULAR"

AFTERHOURS = "AFTERHOURS"

CLOSED = "CLOSED"


# ====================================
# RISK LEVELS
# ====================================

LOW = "LOW"

MEDIUM = "MEDIUM"

HIGH = "HIGH"


# ====================================
# EVENT TYPES
# ====================================

MARKET_UPDATE_EVENT = (
    "MARKET_UPDATE_EVENT"
)

ORDER_SUBMITTED_EVENT = (
    "ORDER_SUBMITTED_EVENT"
)

ORDER_FILLED_EVENT = (
    "ORDER_FILLED_EVENT"
)

ORDER_CANCELLED_EVENT = (
    "ORDER_CANCELLED_EVENT"
)

POSITION_UPDATE_EVENT = (
    "POSITION_UPDATE_EVENT"
)

RISK_ALERT_EVENT = (
    "RISK_ALERT_EVENT"
)

LIQUIDITY_ALERT_EVENT = (
    "LIQUIDITY_ALERT_EVENT"
)

KILL_SWITCH_EVENT = (
    "KILL_SWITCH_EVENT"
)

SYSTEM_ERROR_EVENT = (
    "SYSTEM_ERROR_EVENT"
)


# ====================================
# EXECUTION EVENTS
# ====================================

CHILD_ORDER_CREATED = (
    "CHILD_ORDER_CREATED"
)

CHILD_ORDER_FILLED = (
    "CHILD_ORDER_FILLED"
)

EXECUTION_STARTED = (
    "EXECUTION_STARTED"
)

EXECUTION_COMPLETED = (
    "EXECUTION_COMPLETED"
)


# ====================================
# POSITION MODES
# ====================================

LIVE_POSITIONS = (
    "LIVE_POSITIONS"
)

RUNTIME_POSITIONS = (
    "RUNTIME_POSITIONS"
)


# ====================================
# BROKER TYPES
# ====================================

ALPACA = "ALPACA"

FAKE_BROKER = (
    "FAKE_BROKER"
)

REPLAY_BROKER = (
    "REPLAY_BROKER"
)