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

from core.global_state import (
    system_state
)

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

    system_state.market_state.current_price
)

col2.metric(

    "Spread",

    system_state.market_state.spread
)

col3.metric(

    "Liquidity",

    system_state.market_state.liquidity_score
)

# ====================================
# EXECUTION
# ====================================

st.subheader(
    "Execution"
)

st.write(

    system_state.execution_summary
)

# ====================================
# FILLS
# ====================================

st.subheader(
    "Recent Fills"
)

st.table(

    system_state.fills[-5:]
)

# ====================================
# AI RISK
# ====================================

st.subheader(
    "AI Risk"
)

st.json(

    system_state.ai_risk_result
)

# ====================================
# EXECUTION STATUS
# ====================================

st.subheader(
    "Execution Status"
)

if system_state.execution_halted:

    st.error(

        f"HALTED | "

        f"{system_state.halt_reason}"
    )

else:

    st.success(
        "RUNNING"
    )

# ====================================
# REFRESH BUTTON
# ====================================

if st.button("Refresh Dashboard"):

    st.rerun()