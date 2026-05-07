# 检查/启用规划队列（检测圆圈）
# fsm/states/check_plan_queue.py
import time
from fsm.state import State
from config.settings import PLAN_QUEUE_BUTTON, PLAN_QUEUE_CIRCLE_REGION
import logging
logger = logging.getLogger("GameBot")

class CheckPlanQueueState(State):
    def execute(self, context, controller, recognizer):
        # 方案A：检测圆圈是否存在，如果不存在则点击启用
        has_circle = recognizer.detect_plan_queue_circle(PLAN_QUEUE_CIRCLE_REGION)
        if not has_circle:
            logger.info("规划队列未启用，点击启用")
            controller.safe_click(*PLAN_QUEUE_BUTTON)
            time.sleep(0.5)
        else:
            logger.info("规划队列已启用")
        return "self_improve"