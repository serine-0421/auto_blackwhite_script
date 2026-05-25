# 时间分配（工作时间调4，研究加到最大）
# fsm/states/time_allocate.py
import time
from fsm.state import State
from config.settings import TIME_ALLOC_BUTTON, WORK_TIME_BUTTON, RESEARCH_PLUS_BUTTON, MAX_CLICK_COUNT, YANJIU_BUTTON
import logging
logger = logging.getLogger("GameBot")

class TimeAllocateState(State):
    def execute(self, context, controller, recognizer):
        # 打开时间分配
        controller.safe_click(*TIME_ALLOC_BUTTON)
        time.sleep(1)
        # 设置工作时间 = 4
        logger.info("设置工作时间=4")
        for _ in range(4):
            controller.safe_click(*WORK_TIME_BUTTON)
            time.sleep(0.2)
        # 研究加到最大
        for _ in range(MAX_CLICK_COUNT):
            controller.safe_click(*RESEARCH_PLUS_BUTTON)
            time.sleep(0.1)
        # 关闭时间分配界面（按返回或点击叉）
        controller.press_back()
        time.sleep(0.5)
        # 进入 CheckPlanQueueState 之前，切换到研究队列
        controller.safe_click(*YANJIU_BUTTON)
        time.sleep(0.5)
        return "check_plan_queue"