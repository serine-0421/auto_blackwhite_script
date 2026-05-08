# Reconnect state for the system FSM

import time
from fsm.state import State
from fsm.enums.results import StateResult
from fsm.enums.states import StateType
import logging
logger = logging.getLogger("GameBot")

class ReconnectState(State):
    def execute(self, context, controller, recognizer):
        logger.info("尝试重连设备")
        controller.connector.ensure_connected()
        return StateResult.SUCCESS, StateType.START, None