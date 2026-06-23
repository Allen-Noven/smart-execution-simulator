# ====================================
# analytics.py
# ====================================

from utils.helpers import (
    format_price
)


class ExecutionAnalytics:

    def __init__(

        self,

        slippage_analyzer,

        pnl_tracker,

        benchmark_engine=None

    ):

        # ====================================
        # ANALYTICS MODULES
        # ====================================

        self.slippage_analyzer = (
            slippage_analyzer
        )

        self.pnl_tracker = (
            pnl_tracker
        )

        self.benchmark_engine = (
            benchmark_engine
        )


    # ====================================
    # GET EXECUTION SUMMARY
    # ====================================

    def get_execution_summary(self):

        slippage_records = (

            self.slippage_analyzer.records
        )

        pnl_tracker = (
            self.pnl_tracker
        )


        # ====================================
        # SLIPPAGE SUMMARY
        # ====================================

        total_slippage = sum(

            record["slippage"]

            for record in slippage_records
        )


        total_bps = sum(

            record["slippage_bps"]

            for record in slippage_records
        )


        total_execution_cost = sum(

            record["execution_cost"]

            for record in slippage_records
        )


        total_records = (
            len(slippage_records)
        )


        avg_slippage = 0

        avg_bps = 0


        if total_records > 0:

            avg_slippage = (

                total_slippage
                / total_records
            )

            avg_bps = (

                total_bps
                / total_records
            )


        # ====================================
        # BUILD SUMMARY
        # ====================================

        summary = {

            "total_executions":
            total_records,

            "average_slippage":
            round(avg_slippage, 4),

            "average_bps":
            round(avg_bps, 2),

            "total_execution_cost":
            round(
                total_execution_cost,
                2
            ),

            "position":
            pnl_tracker.position,

            "average_price":
            round(
                pnl_tracker.average_price,
                4
            ),

            "realized_pnl":
            round(
                pnl_tracker.realized_pnl,
                2
            ),

            "unrealized_pnl":
            round(
                pnl_tracker.unrealized_pnl,
                2
            )
        }

        return summary


    # ====================================
    # SHOW EXECUTION SUMMARY
    # ====================================

    def show_summary(self):

        summary = (
            self.get_execution_summary()
        )

        print(

            "\n========== EXECUTION ANALYTICS ==========\n"
        )

        print(

            f"Total Executions: "
            f"{summary['total_executions']}"
        )

        print(

            f"Average Slippage: "
            f"{summary['average_slippage']}"
        )

        print(

            f"Average BPS: "
            f"{summary['average_bps']}"
        )

        print(

            f"Execution Cost: "
            f"{summary['total_execution_cost']}"
        )

        print(

            f"Position: "
            f"{summary['position']}"
        )

        print(

            f"Average Price: "
            f"{summary['average_price']}"
        )

        print(

            f"Realized PnL: "
            f"{summary['realized_pnl']}"
        )

        print(

            f"Unrealized PnL: "
            f"{summary['unrealized_pnl']}"
        )

        print(

            "\n=========================================\n"
        )