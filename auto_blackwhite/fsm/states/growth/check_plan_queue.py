# 检查/启用规划队列（检测圆圈）

import time
from fsm.state import State
from config.settings import PLAN_QUEUE_CIRCLE_REGION, YANJIU_BUTTON, LIFE_BUTTON, GUIHUADUILIE
import logging
logger = logging.getLogger("GameBot")

class CheckPlanQueueState(State):
    def execute(self, context, controller, recognizer):
        has_circle = recognizer.detect_plan_queue_circle(PLAN_QUEUE_CIRCLE_REGION)
        if has_circle:
            logger.info("规划队列已启用")
            return "self_improve"

        logger.warning(
            "规划队列圆圈未检测到，可能未进入正确页面或坐标需校准，开始修复流程"
        )
        recognizer.save_debug_screenshot(
            PLAN_QUEUE_CIRCLE_REGION,
            prefix="check_plan_queue_fail_1"
        )

        controller.safe_click(*LIFE_BUTTON)
        time.sleep(0.5)
        controller.safe_click(*YANJIU_BUTTON)
        time.sleep(0.5)

        has_circle = recognizer.detect_plan_queue_circle(PLAN_QUEUE_CIRCLE_REGION)
        if has_circle:
            logger.info("规划队列修复成功（LIFE_BUTTON + YANJIU_BUTTON），进入下一流程")
            return "self_improve"

        logger.warning("规划队列修复失败，尝试点击GUIHUADUILIE后重新检测")
        recognizer.save_debug_screenshot(
            PLAN_QUEUE_CIRCLE_REGION,
            prefix="check_plan_queue_fail_2"
        )

        controller.safe_click(*GUIHUADUILIE)
        time.sleep(0.5)

        has_circle = recognizer.detect_plan_queue_circle(PLAN_QUEUE_CIRCLE_REGION)
        if has_circle:
            logger.info("规划队列修复成功（GUIHUADUILIE），进入下一流程")
            return "self_improve"

        logger.warning("规划队列修复仍然失败，继续进入下一流程")
        recognizer.save_debug_screenshot(
            PLAN_QUEUE_CIRCLE_REGION,
            prefix="check_plan_queue_fail_3"
        )
        return "self_improve"
