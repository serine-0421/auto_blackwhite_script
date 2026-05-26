# 雇佣研究助理，确认支出503
# fsm/states/hire_assistant.py
import time
from fsm.state import State
from config.settings import DAILY_BUTTON, EMPLOY_BUTTON, RESEARCH_ASSISTANT, EXPENDITURE_REGION, TARGET_EXPENDITURE
import logging
logger = logging.getLogger("GameBot")

class HireAssistantState(State):
    def execute(self, context, controller, recognizer):
        # 进入生活->雇佣
        controller.safe_click(*DAILY_BUTTON)
        time.sleep(0.5)
        controller.safe_click(*EMPLOY_BUTTON)
        time.sleep(0.5)
        controller.safe_click(*RESEARCH_ASSISTANT)
        time.sleep(1)
        # 截图支出区域
        exp = recognizer.ocr_number(EXPENDITURE_REGION)
        if exp == TARGET_EXPENDITURE:
            context.expenditure = exp
            logger.info("雇佣成功，支出503")
            # 返回主界面（可能需要多次返回）
            for _ in range(3):
                controller.press_back()
                time.sleep(0.5)
            # 先切换到工作-科研界面，再检查规划队列和后续等级
            return "switch_to_work"
        else:
            logger.warning(f"支出{exp}不等于503，重试")
            # 记录错误日志
            # 回到check_income重新净收入检测
            for _ in range(3):
                controller.press_back()
            return "check_income"