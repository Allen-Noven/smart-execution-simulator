# ====================================
# logger.py
# ====================================

import os

from datetime import datetime

import pytz

from utils.config import (

    MARKET_TIMEZONE,

    LOG_LEVEL
)


# ====================================
# TIMEZONE
# ====================================

MARKET_TZ = pytz.timezone(
    MARKET_TIMEZONE
)


# ====================================
# LOG DIRECTORY
# ====================================

LOG_DIR = "logs"

os.makedirs(

    LOG_DIR,

    exist_ok=True
)


# ====================================
# LOGGER
# ====================================

class SystemLogger:


    def __init__(self):

        self.log_file = (

            f"{LOG_DIR}/"

            f"execution.log"
        )


    # ====================================
    # CURRENT TIME
    # ====================================

    def _current_time(self):

        return datetime.now(
            MARKET_TZ
        )


    # ====================================
    # FORMAT MESSAGE
    # ====================================

    def _format_message(

        self,

        level,

        message
    ):

        return (

            f"[{level}] "

            f"{self._current_time()} "

            f"{message}"
        )


    # ====================================
    # WRITE LOG
    # ====================================

    def _write_log(

        self,

        formatted_message
    ):

        with open(

            self.log_file,

            "a"
        ) as file:

            file.write(

                formatted_message
                + "\n"
            )


    # ====================================
    # INFO
    # ====================================

    def info(

        self,

        message
    ):

        formatted_message = (

            self._format_message(

                "INFO",

                message
            )
        )

        print(
            formatted_message
        )

        self._write_log(
            formatted_message
        )


    # ====================================
    # WARNING
    # ====================================

    def warning(

        self,

        message
    ):

        formatted_message = (

            self._format_message(

                "WARNING",

                message
            )
        )

        print(
            formatted_message
        )

        self._write_log(
            formatted_message
        )


    # ====================================
    # ERROR
    # ====================================

    def error(

        self,

        message
    ):

        formatted_message = (

            self._format_message(

                "ERROR",

                message
            )
        )

        print(
            formatted_message
        )

        self._write_log(
            formatted_message
        )


    # ====================================
    # DEBUG
    # ====================================

    def debug(

        self,

        message
    ):

        if LOG_LEVEL != "DEBUG":

            return

        formatted_message = (

            self._format_message(

                "DEBUG",

                message
            )
        )

        print(
            formatted_message
        )

        self._write_log(
            formatted_message
        )