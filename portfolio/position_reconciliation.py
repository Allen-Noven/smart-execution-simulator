# ====================================
# position_reconciliation.py
# ====================================

from utils.logger import (
    SystemLogger
)

from utils.helpers import (
    format_price
)


class PositionReconciliation:


    # ====================================
    # INIT
    # ====================================

    def __init__(

        self,

        internal_position_manager,

        broker_positions
    ):

        self.logger = (
            SystemLogger()
        )

        self.internal_position_manager = (
            internal_position_manager
        )

        self.broker_positions = (
            broker_positions
        )


    # ====================================
    # RECONCILE POSITIONS
    # ====================================

    def reconcile_positions(self):

        internal_positions = (

            self.internal_position_manager
            .get_all_positions()
        )

        broker_positions = (

            self.broker_positions
            .get_all_positions()
        )

        reconciliation_results = []


        # ====================================
        # GET ALL SYMBOLS
        # ====================================

        all_symbols = set(

            list(internal_positions.keys())

            +

            list(broker_positions.keys())
        )


        # ====================================
        # COMPARE POSITIONS
        # ====================================

        for symbol in all_symbols:

            internal_qty = (

                internal_positions
                .get(symbol, {})
                .get("qty", 0)
            )

            broker_qty = (

                broker_positions
                .get(symbol, {})
                .get("qty", 0)
            )

            qty_difference = (

                internal_qty
                - broker_qty
            )

            is_matched = (
                qty_difference == 0
            )

            reconciliation_results.append({

                "symbol":
                symbol,

                "internal_qty":
                internal_qty,

                "broker_qty":
                broker_qty,

                "difference":
                qty_difference,

                "matched":
                is_matched
            })


            # ====================================
            # LOG RESULT
            # ====================================

            if is_matched:

                self.logger.info(

                    f"[RECONCILIATION] "

                    f"{symbol} matched"
                )

            else:

                self.logger.warning(

                    f"[RECONCILIATION] "

                    f"{symbol} mismatch | "

                    f"Internal: "
                    f"{internal_qty} | "

                    f"Broker: "
                    f"{broker_qty}"
                )

        return reconciliation_results


    # ====================================
    # GET MISMATCHES
    # ====================================

    def get_mismatches(self):

        reconciliation_results = (
            self.reconcile_positions()
        )

        mismatches = []

        for result in reconciliation_results:

            if not result["matched"]:

                mismatches.append(result)

        return mismatches


    # ====================================
    # HAS MISMATCH
    # ====================================

    def has_mismatch(self):

        mismatches = (
            self.get_mismatches()
        )

        return len(mismatches) > 0


    # ====================================
    # SHOW RECONCILIATION REPORT
    # ====================================

    def show_reconciliation_report(self):

        reconciliation_results = (
            self.reconcile_positions()
        )

        print(

            "\n========== "
            "POSITION RECONCILIATION "
            "==========\n"
        )

        for result in reconciliation_results:

            print(

                f"{result['symbol']} | "

                f"Internal: "
                f"{result['internal_qty']} | "

                f"Broker: "
                f"{result['broker_qty']} | "

                f"Difference: "
                f"{result['difference']} | "

                f"Matched: "
                f"{result['matched']}"
            )

        print(

            "\n==============================="
            "===================\n"
        )