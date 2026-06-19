# ====================================
# logger.py
# ====================================

from datetime import datetime


class SystemLogger:

    def __init__(self):

        pass


    # ====================================
    # INFO
    # ====================================

    def info(

        self,

        message

    ):

        print(

            f"[INFO] "

            f"{datetime.now()} "

            f"{message}"
        )


    # ====================================
    # WARNING
    # ====================================

    def warning(

        self,

        message

    ):

        print(

            f"[WARNING] "

            f"{datetime.now()} "

            f"{message}"
        )


    # ====================================
    # ERROR
    # ====================================

    def error(

        self,

        message

    ):

        print(

            f"[ERROR] "

            f"{datetime.now()} "

            f"{message}"
        )