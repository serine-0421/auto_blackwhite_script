# 时间分配（工作时间调4，研究加到最大）
# fsm/states/time_allocate.py
import time
from fsm.state import State
from config.settings import TIME_ALLOC_BUTTON, WORK_TIME_SLIDER, RESEARCH_PLUS_BUTTON, MAX_CLICK_COUNT
import logging
logger = logging.getLogger("GameBot")

class TimeAllocateState(State):
    def execute(self, context, controller, recognizer):
        # 打开时间分配
        controller.safe_click(*TIME_ALLOC_BUTTON)
        time.sleep(1)
        # 设置工作时间 = 4
        # 假设滑动条可以拖动，或者按钮加减；这里简化，直接点击工作时间的增加按钮? 
        # 视具体界面而定。暂用点击滑块坐标，实际可能需要多次点击降低或增加
        # 按照用户描述：工作时间调到4，可能需要多次点击+或-。这里提供框架，具体需调
        # 假设有减号按钮，一直减到4
        # 真实实现需要根据坐标调整，此处占位
        logger.info("设置工作时间=4")
        # 研究加到最大
        for _ in range(MAX_CLICK_COUNT):
            controller.safe_click(*RESEARCH_PLUS_BUTTON)
            time.sleep(0.1)
        # 关闭时间分配界面（按返回或点击叉）
        controller.press_back()
        time.sleep(0.5)
        return "check_plan_queue"