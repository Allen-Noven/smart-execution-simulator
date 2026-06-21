# ====================================
# app.py
# ====================================

import sys
import os

# ====================================
# ADD PROJECT ROOT TO PYTHON PATH
# ====================================

PROJECT_ROOT = os.path.dirname(

    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(PROJECT_ROOT)

import streamlit as st

# ====================================
# INITIALIZE REDIS STATE
# ====================================


from core.redis_state import RedisState
redis_state = RedisState()

# ====================================
# PAGE CONFIG
# ====================================

st.set_page_config(

    page_title=
    "Smart Execution Dashboard",

    layout="wide"
)

# ====================================
# AUTO REFRESH
# ====================================

st_autorefresh = st.empty()

# ====================================
# TITLE
# ====================================

st.title(
    "AI Smart Execution Platform"
)

# ====================================
# MARKET DATA FROM REDIS
# ====================================


market_data = redis_state.get_market_state(
    "NVDA"
)
ai_risk = redis_state.get_ai_risk_result()
execution_summary = (
    redis_state.get_execution_summary()
)

fills = redis_state.get_fills()

execution_status = (
    redis_state.get_execution_status()
)

alerts = redis_state.get_alerts()
market_data = redis_state.get_market_state(
    "NVDA"
)

ai_risk = redis_state.get_ai_risk_result()

execution_summary = (
    redis_state.get_execution_summary()
)

fills = redis_state.get_fills()

execution_status = (
    redis_state.get_execution_status()
)

alerts = redis_state.get_alerts()

# ====================================
# DEFAULT MARKET DATA
# ====================================

if market_data is None:

    market_data = {

        "price": 0,

        "spread": 0,

        "liquidity": 0
    }

# ====================================
# DEFAULT AI RISK
# ====================================

if ai_risk is None:

    ai_risk = {

        "severity": "UNKNOWN",

        "reason": "No AI risk data"
    }

# ====================================
# DEFAULT EXECUTION SUMMARY
# ====================================

if execution_summary is None:

    execution_summary = {

        "strategy": "N/A",

        "filled_qty": 0,

        "remaining_qty": 0,

        "completion": 0
    }

# ====================================
# DEFAULT EXECUTION STATUS
# ====================================

if execution_status is None:

    execution_status = {

        "status": "UNKNOWN",

        "halted": False,

        "reason": None
    }

# ====================================
# MARKET STATE
# ====================================

st.subheader(
    "Market State"
)


col1, col2, col3 = (
    st.columns(3)
)

col1.metric(

    "Price",

    market_data["price"]
)

col2.metric(

    "Spread",

    market_data["spread"]
)

col3.metric(

    "Liquidity",

    market_data["liquidity"]
)

# ====================================
# EXECUTION
# ====================================

st.subheader(
    "Execution"
)

st.write(execution_summary)

# ====================================
# FILLS
# ====================================

st.subheader(
    "Recent Fills"
)

st.table(fills[-5:])

# ====================================
# AI RISK
# ====================================

st.subheader(
    "AI Risk"
)

st.json(ai_risk)

# ====================================
# EXECUTION STATUS
# ====================================

if execution_status:
    
    st.subheader(
        "Execution Status"
    )

    if execution_status["halted"]:

        st.error(

            f"HALTED | "

            f"{execution_status['reason']}"
        )

    else:

        st.success(

            execution_status["status"]
        )
# ====================================
# ALERTS
# ====================================

st.subheader(
    "Alerts"
)

if len(alerts) == 0:

    st.success(
        "No Active Alerts"
    )

else:

    for alert in alerts[-5:]:

        st.warning(alert)
# ====================================
# REFRESH BUTTON
# ====================================

if st.button("Refresh Dashboard"):

    st.rerun()