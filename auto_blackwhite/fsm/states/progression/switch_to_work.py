# 切换到工作→科研界面
# fsm/states/switch_to_work.py
import time
from fsm.state import State
from config.settings import WORK_BUTTON, RESEARCH_TAB, YANJIUSHENG
import logging
logger = logging.getLogger("GameBot")

class SwitchToWorkState(State):
    def execute(self, context, controller, recognizer):
        # 点击“工作”
        controller.safe_click(*WORK_BUTTON)
        time.sleep(0.5)
        # 再点击“科研”
        controller.safe_click(*RESEARCH_TAB)
        time.sleep(0.5)
        if getattr(context, 'click_research_student', False):
            logger.info("识别活力研究等级失败，点击研究生按钮继续后续流程")
            controller.safe_click(*YANJIUSHENG)
            time.sleep(0.5)
            context.click_research_student = False
        # 接下来需要再次检查规划队列（根据流程）
        logger.info("已切换到工作-科研界面")
        return "check_plan_queue"
