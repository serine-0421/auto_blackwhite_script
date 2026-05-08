# Recovery state for the system FSM

import time
from fsm.state import State
from fsm.enums.results import StateResult
from fsm.enums.states import StateType
import logging
logger = logging.getLogger("GameBot")

class RecoveryState(State):
    def execute(self, context, controller, recognizer):
        logger.info("进入恢复模式，尝试返回主界面")
        # 连续按返回键多次
        for _ in range(5):
            controller.press_back()
            time.sleep(0.5)
        # 检查模拟器状态
        return StateResult.SUCCESS, StateType.START, None