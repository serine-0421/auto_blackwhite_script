# Watchdog state for the system FSM

import time
from fsm.state import State
from fsm.enums.results import StateResult
from fsm.enums.states import StateType
import logging
logger = logging.getLogger("GameBot")

class WatchdogState(State):
    def execute(self, context, controller, recognizer):
        # 监控模拟器进程，实现检查ADB连接
        try:
            controller.connector.ensure_connected()
            return StateResult.SUCCESS, StateType.START, None
        except:
            return StateResult.ERROR, StateType.RECONNECT, None