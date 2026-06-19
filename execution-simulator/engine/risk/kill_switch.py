# ====================================
# kill_switch.py
# ====================================

from utils.helpers import (
    get_current_time
)

from utils.logger import (
    SystemLogger
)

from services.email_service import (
    EmailService
)

from utils.constants import (

    HALTED,

    RUNNING,

    KILL_SWITCH_EVENT
)


class KillSwitch:

    def __init__(

        self,

        scheduler=None,

        oms=None,

        system_state=None,

        event_bus=None

    ):

        # ====================================
        # LOGGER
        # ====================================

        self.logger = (
            SystemLogger()
        )

        # ====================================
        # EMAIL SERVICE
        # ====================================

        self.email_service = (
            EmailService()
        )

        # ====================================
        # EVENT BUS
        # ====================================

        self.event_bus = (
            event_bus
        )

        # ====================================
        # SHARED COMPONENTS
        # ====================================

        self.scheduler = (
            scheduler
        )

        self.oms = oms

        self.system_state = (
            system_state
        )

        # ====================================
        # EXECUTION STATE
        # ====================================

        self.execution_halted = False

        self.halt_reason = None

        # ====================================
        # AUDIT TRAIL
        # ====================================

        self.events = []


    # ====================================
    # HALT EXECUTION
    # ====================================

    def halt_execution(

        self,

        reason,

        trigger_source="UNKNOWN"

    ):

        self.execution_halted = True

        self.halt_reason = reason

        # ====================================
        # STOP SCHEDULER
        # ====================================

        if self.scheduler:

            self.scheduler.stop()

        # ====================================
        # UPDATE SYSTEM STATE
        # ====================================

        if self.system_state:

            self.system_state.execution_halted = (
                True
            )

            self.system_state.halt_reason = (
                reason
            )

            self.system_state.execution_status = (
                HALTED
            )

        # ====================================
        # AUDIT EVENT
        # ====================================

        event = {

            "timestamp":
            get_current_time(),

            "trigger_source":
            trigger_source,

            "reason":
            reason
        }

        self.events.append(
            event
        )

        # ====================================
        # LOG EVENT
        # ====================================

        self.logger.critical(

            f"KILL SWITCH ACTIVATED | "

            f"{reason}"
        )

        # ====================================
        # EMAIL ALERT
        # ====================================

        self.email_service.send_kill_switch_alert(

            symbol="SYSTEM",

            reason=reason
        )

        # ====================================
        # PUBLISH EVENT
        # ====================================

        if self.event_bus:

            self.event_bus.publish(

                KILL_SWITCH_EVENT,

                {

                    "halted": True,

                    "reason": reason
                }
            )


    # ====================================
    # RESUME EXECUTION
    # ====================================

    def resume_execution(self):

        self.execution_halted = False

        self.halt_reason = None

        # ====================================
        # RESUME SCHEDULER
        # ====================================

        if self.scheduler:

            self.scheduler.resume()

        # ====================================
        # UPDATE SYSTEM STATE
        # ====================================

        if self.system_state:

            self.system_state.execution_halted = (
                False
            )

            self.system_state.halt_reason = None

            self.system_state.execution_status = (
                RUNNING
            )

        self.logger.warning(
            "Execution Resumed"
        )


    # ====================================
    # EVENT CALLBACK
    # ====================================

    def on_ai_risk(

        self,

        ai_result

    ):

        self.process_ai_risk(
            ai_result
        )


    # ====================================
    # CHECK HALT STATUS
    # ====================================

    def is_halted(self):

        return self.execution_halted


    # ====================================
    # GET HALT REASON
    # ====================================

    def get_halt_reason(self):

        return self.halt_reason


    # ====================================
    # GET AUDIT EVENTS
    # ====================================

    def get_events(self):

        return self.events


    # ====================================
    # PROCESS AI RESULT
    # ====================================

    def process_ai_risk(

        self,

        ai_result

    ):

        if ai_result is None:

            return

        severity = (
            ai_result["severity"]
        )

        halt_execution = (
            ai_result["halt_execution"]
        )

        reason = (
            ai_result["reason"]
        )

        recommended_action = (

            ai_result.get(
                "recommended_action",
                "MONITOR"
            )
        )

        # ====================================
        # HARD HALT
        # ====================================

        if (

            severity == "HIGH"
            and
            halt_execution

        ):

            self.halt_execution(

                reason=reason,

                trigger_source=
                "AI_RISK_ENGINE"
            )

        # ====================================
        # REDUCE AGGRESSION
        # ====================================

        elif recommended_action == (

            "REDUCE_AGGRESSION"
        ):

            self.logger.warning(

                "AI recommends reducing "
                "execution aggression."
            )

        # ====================================
        # SWITCH TO ICEBERG
        # ====================================

        elif recommended_action == (

            "SWITCH_TO_ICEBERG"
        ):

            self.logger.warning(

                "AI recommends switching "
                "to ICEBERG execution."
            )

        else:

            self.logger.info(

                "Risk Level Acceptable | "
                "Execution Continues"
            )
