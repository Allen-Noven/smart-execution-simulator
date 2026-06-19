# ====================================
# config.py
# ====================================

import os


# ====================================
# ENVIRONMENT
# ====================================

PAPER_TRADING = True

DATA_MODE = "replay"

# replay
# live


# ====================================
# ALPACA API CONFIG
# ====================================

API_KEY = os.getenv(
    "PKS775Q3SDJJEI5G5JUOHX5MNZ"
)

SECRET_KEY = os.getenv(
    "6ZQr11bvF52WoxT9uheVX3sSMWCALfmCHChhoCaRvFQG"
)


# ====================================
# FINNHUB CONFIG
# ====================================

FINNHUB_API_KEY = os.getenv(
    "d8psfupr01qtgb4j2dngd8psfupr01qtgb4j2do0"
)

NEWS_PROVIDER = "finnhub"


# ====================================
# DEEPSEEK CONFIG
# ====================================

DEEPSEEK_API_KEY = os.getenv(
    "sk-a5fd95bc870143afb3ff911b20c1d441"
)


# ====================================
# EMAIL CONFIG
# ====================================

EMAIL_SENDER = os.getenv(
    "EMAIL_SENDER"
)

EMAIL_PASSWORD = os.getenv(
    "EMAIL_PASSWORD"
)

PM_EMAIL = os.getenv(
    "PM_EMAIL"
)

TRADER_EMAIL = os.getenv(
    "TRADER_EMAIL"
)


# ====================================
# TRADING CONFIG
# ====================================

DEFAULT_SYMBOL = "NVDA"

WATCHLIST = [

    "NVDA",

    "AAPL",

    "MSFT"
]

DEFAULT_ORDER_QTY = 1


# ====================================
# EXECUTION CONFIG
# ====================================

EXECUTION_INTERVAL = 5

DEFAULT_PARTICIPATION = 0.10


# ====================================
# RISK CONFIG
# ====================================

MAX_ORDER_SIZE = 10

MAX_POSITION_SIZE = 100

MAX_NOTIONAL = 100000

MAX_PARTICIPATION = 0.20


# ====================================
# LIQUIDITY CONFIG
# ====================================

SPREAD_THRESHOLD = 0.05

MIN_VOLUME = 1000


# ====================================
# MARKET DATA CONFIG
# ====================================

REALTIME_REFRESH_RATE = 1


# ====================================
# DASHBOARD CONFIG
# ====================================

DASHBOARD_TITLE = (

    "Allen's Smart Execution System"
)