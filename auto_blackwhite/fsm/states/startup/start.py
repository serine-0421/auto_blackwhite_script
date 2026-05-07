# 初始状态（检测是否在开局选天赋）
# fsm/states/start.py
import time
from fsm.state import State
import logging
logger = logging.getLogger("GameBot")

class StartState(State):
    def execute(self, context, controller, recognizer):
        # 检测是否在选天赋界面或主界面，如果是则进入选天赋状态
        # 这里简化为直接进入选天赋，实际可加检测逻辑
        logger.info("检测游戏启动，准备选天赋")
        return "select_talent"