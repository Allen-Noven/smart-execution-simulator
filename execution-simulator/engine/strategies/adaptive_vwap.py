# ====================================
# adaptive_vwap.py
# ====================================

from utils.logger import (
    SystemLogger
)


class AdaptiveVWAPStrategy:

    def __init__(

        self,

        total_qty,

        target_participation,

        market_state=None,

        max_child_qty=None

    ):

        # ====================================
        # LOGGER
        # ====================================

        self.logger = (
            SystemLogger()
        )


        # ====================================
        # EXECUTION TARGET
        # ====================================

        self.total_qty = (
            total_qty
        )

        self.remaining_qty = (
            total_qty
        )

        self.executed_qty = 0


        # ====================================
        # PARTICIPATION
        # ====================================

        self.base_participation = (
            target_participation
        )

        self.target_participation = (
            target_participation
        )


        # ====================================
        # EXECUTION LIMITS
        # ====================================

        self.max_child_qty = (
            max_child_qty
        )


        # ====================================
        # MARKET STATE
        # ====================================

        self.market_state = (
            market_state
        )


        # ====================================
        # EXECUTION TRACKING
        # ====================================

        self.slice_id = 0


    # ====================================
    # ADAPT PARTICIPATION
    # ====================================

    def adjust_participation(self):

        if self.market_state is None:

            return


        volatility = (
            self.market_state.volatility
        )

        liquidity_score = (
            self.market_state.liquidity_score
        )

        spread = (
            self.market_state.spread
        )


        adjusted = (
            self.base_participation
        )


        # ====================================
        # HIGH VOLATILITY
        # ====================================

        if (

            volatility is not None
            and
            volatility > 0.05

        ):

            adjusted *= 0.7


        # ====================================
        # LOW LIQUIDITY
        # ====================================

        if (

            liquidity_score is not None
            and
            liquidity_score < 50

        ):

            adjusted *= 0.6


        # ====================================
        # WIDE SPREAD
        # ====================================

        if (

            spread is not None
            and
            spread > 0.10

        ):

            adjusted *= 0.7


        self.target_participation = (
            adjusted
        )


    # ====================================
    # NEXT CHILD ORDER
    # ====================================

    def get_next_order(

        self,

        market_volume=None

    ):

        # ====================================
        # USE MARKET STATE
        # ====================================

        if (

            market_volume is None
            and
            self.market_state is not None

        ):

            market_volume = (

                self.market_state
                .current_volume
            )


        if (

            market_volume is None
            or
            market_volume <= 0

        ):

            self.logger.warning(

                "No market volume available"
            )

            return None


        # ====================================
        # ADAPT EXECUTION
        # ====================================

        self.adjust_participation()


        # ====================================
        # CHILD ORDER SIZE
        # ====================================

        child_qty = int(

            market_volume
            *
            self.target_participation
        )


        # ====================================
        # MAX CHILD LIMIT
        # ====================================

        if self.max_child_qty:

