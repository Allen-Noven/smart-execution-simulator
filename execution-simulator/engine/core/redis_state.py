# ====================================
# redis_state.py
# ====================================

import json
import redis


class RedisState:

    def __init__(self):

        self.redis_client = redis.Redis(

            host="localhost",

            port=6379,

            decode_responses=True
        )


    # ====================================
    # MARKET STATE
    # ====================================

    def set_market_state(

        self,

        symbol,

        data

    ):

        self.redis_client.set(

            f"market:{symbol}",

            json.dumps(data)
        )


    def get_market_state(

        self,

        symbol

    ):

        data = self.redis_client.get(

            f"market:{symbol}"
        )

        if data:

            return json.loads(data)

        return None


    # ====================================
    # SYSTEM STATE
    # ====================================

    def set_system_state(

        self,

        data

    ):

        self.redis_client.set(

            "system_state",

            json.dumps(data)
        )


    def get_system_state(self):

        data = self.redis_client.get(

            "system_state"
        )

        if data:

            return json.loads(data)

        return None
    # ====================================
# FILLS
# ====================================

    def set_fills(

        self,

        fills

    ):

        self.redis_client.set(

            "fills",

            json.dumps(fills, default= str)
        )


    def get_fills(self):

        data = self.redis_client.get(
            "fills"
        )

        if data:

            return json.loads(data)

        return []
# ====================================
# AI RISK
# ====================================

    def set_ai_risk_result(

        self,

        data

    ):

        self.redis_client.set(

            "ai_risk_result",

            json.dumps(data)
        )


    def get_ai_risk_result(self):

        data = self.redis_client.get(

            "ai_risk_result"
        )

        if data:

            return json.loads(data)

        return None
    # ====================================
    # ALERTS
    # ====================================

    def set_alerts(

        self,

        alerts

    ):

        self.redis_client.set(

            "alerts",

            json.dumps(alerts)
        )


    def get_alerts(self):

        data = self.redis_client.get(
            "alerts"
        )

        if data:

            return json.loads(data)

        return []
    # ====================================
    # EXECUTION STATUS
    # ====================================

    def set_execution_status(

        self,

        status_data

    ):

        self.redis_client.set(

            "execution_status",

            json.dumps(status_data)
        )


    def get_execution_status(self):

        data = self.redis_client.get(
            "execution_status"
        )

        if data:

            return json.loads(data)

        return {}
    # ====================================
    # EXECUTION SUMMARY
    # ====================================

    def set_execution_summary(

        self,

        summary

    ):

        self.redis_client.set(

            "execution_summary",

            json.dumps(

                summary,

                default=str
            )
        )


    def get_execution_summary(self):

        data = self.redis_client.get(
            "execution_summary"
        )

        if data:

            return json.loads(data)

        return {}
