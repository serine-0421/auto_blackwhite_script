# 检查/启用规划队列（检测圆圈）

import time
from fsm.state import State
from config.settings import PLAN_QUEUE_CIRCLE_REGION
import logging
logger = logging.getLogger("GameBot")

class CheckPlanQueueState(State):
    def execute(self, context, controller, recognizer):
        has_circle = recognizer.detect_plan_queue_circle(PLAN_QUEUE_CIRCLE_REGION)
        if not has_circle:
            logger.warning("规划队列圆圈未检测到，可能未进入正确页面或坐标需校准")
        else:
            logger.info("规划队列已启用")
        return "self_improve"