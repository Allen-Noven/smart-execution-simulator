# ====================================
# execution_api# execution_api.py

from fastapi import (
    FastAPI,
    WebSocket
)

from pydantic import BaseModel

from execution.execution_service import (
    ExecutionService
)

from execution.oms.fake_oms import (
    FakeOMS
)

from utils.logger import (
    SystemLogger
)

from core.parent_order import (
    ParentOrder
)


# ====================================
# LOGGER
# ====================================

logger = SystemLogger()


# ====================================
# FASTAPI APP
# ====================================

app = FastAPI()


# ====================================
# OMS
# ====================================

oms = FakeOMS()


# ====================================
# EXECUTION SERVICE
# ====================================

execution_service = ExecutionService(
    oms=oms
)


# ====================================
# WEBSOCKET CONNECTIONS
# ====================================

active_connections = []


# ====================================
# ORDER REQUEST MODEL
# ====================================

class OrderRequest(BaseModel):

    symbol: str

    qty: float

    side: str


# ====================================
# HEALTH CHECK
# ====================================

@app.get("/health")
def health():

    return {

        "status": "running"
    }


# ====================================
# WEBSOCKET
# ====================================

@app.websocket("/ws")

async def websocket_endpoint(

    websocket: WebSocket
):

    await websocket.accept()

    active_connections.append(
        websocket
    )

    logger.info(
        "WebSocket Client Connected"
    )

    try:

        while True:

            await websocket.receive_text()

    except Exception:

        if websocket in active_connections:

            active_connections.remove(
                websocket
            )

        logger.warning(
            "WebSocket Client Disconnected"
        )


# ====================================
# BROADCAST EVENT
# ====================================

async def broadcast_event(

    event,

    payload
):

    message = {

        "event":
        event,

        "payload":
        payload
    }

    disconnected = []

    for connection in active_connections:

        try:

            await connection.send_json(
                message
            )

        except Exception:

            disconnected.append(
                connection
            )

    for connection in disconnected:

        if connection in active_connections:

            active_connections.remove(
                connection
            )


# ====================================
# SUBMIT ORDER
# ====================================

@app.post("/orders")

def submit_order(

    order: OrderRequest
):

    logger.info(

        f"External PM Order | "

        f"{order.symbol} | "

        f"{order.qty}"
    )

    try:

        # ====================================
        # CREATE PARENT ORDER
        # ====================================

        parent_order = (

            ParentOrder(

                symbol=order.symbol,

                side=order.side,

                quantity=order.qty,

                strategy="VWAP"
            )
        )

        # ====================================
        # EXECUTE ORDER
        # ====================================

        result = (

            execution_service
            .submit_order(

                parent_order
            )
        )

        # ====================================
        # WEBSOCKET ORDER UPDATE
        # ====================================

        asyncio.run(

            broadcast_event(

                "ORDER_UPDATE",

                {

                    "symbol":
                    order.symbol,

                    "qty":
                    order.qty,

                    "side":
                    order.side,

                    "status":
                    result.get(
                        "status",
                        "UNKNOWN"
                    ),

                    "order_id":
                    result.get(
                        "order_id"
                    )
                }
            )
        )

        # ====================================
        # WEBSOCKET EXECUTION COMPLETE
        # ====================================

        asyncio.run(

            broadcast_event(

                "EXECUTION_COMPLETED",

                {

                    "symbol":
                    order.symbol,

                    "qty":
                    order.qty,

                    "side":
                    order.side
                }
            )
        )

        return {

            "accepted": True,

            "symbol":
            order.symbol,

            "qty":
            order.qty,

            "side":
            order.side,

            "result":
            result
        }

    except Exception as error:

        logger.error(

            f"Execution API Failed | "

            f"{error}"
        )

        asyncio.run(

            broadcast_event(

                "RISK_ALERT",

                {

                    "message":
                    str(error)
                }
            )
        )

        return {

            "accepted": False,

            "error":
            str(error)
        }


# ====================================
# GET POSITIONS
# ====================================

@app.get("/positions")

def get_positions():

    return (

        execution_service
        .get_positions()
    )


# ====================================
# GET ACTIVE ORDERS
# ====================================

@app.get("/active-orders")

def get_active_orders():

    return (

        execution_service
        .get_active_orders()
    )


# ====================================
# GET PORTFOLIO
# ====================================

@app.get("/portfolio")

def get_portfolio():

    return (

        execution_service
        .get_portfolio_summary()
    )

# ====================================

