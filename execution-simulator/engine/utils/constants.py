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

ICEBERG = "ICEBERG"

ADAPTIVE_TWAP = (
    "ADAPTIVE_TWAP"
)


# ====================================
# RISK LEVELS
# ====================================

LOW = "LOW"

MEDIUM = "MEDIUM"

HIGH = "HIGH"


# ====================================
# EXECUTION STATUS
# ====================================

RUNNING = "RUNNING"

HALTED = "HALTED"

COMPLETED = "COMPLETED"
# ====================================
# EVENT TYPES
# ====================================

MARKET_UPDATE_EVENT = (
    "MARKET_UPDATE_EVENT"
)

NEWS_EVENT = (
    "NEWS_EVENT"
)

AI_RISK_EVENT = (
    "AI_RISK_EVENT"
)

KILL_SWITCH_EVENT = (
    "KILL_SWITCH_EVENT"
)