# 检查净收入（<500循环，>=500去雇佣）
# fsm/states/check_income.py
import time
from fsm.state import State
from config.settings import INCOME_REGION, INCOME_THRESHOLD
import logging
logger = logging.getLogger("GameBot")

class CheckIncomeState(State):
    def execute(self, context, controller, recognizer):
        # 截图净收入区域
        income = recognizer.ocr_number(INCOME_REGION)
        if income == -1:
            logger.warning("净收入识别失败，等待重试")
            time.sleep(3)
            return None  # 留在本状态
        context.net_income = income
        logger.info(f"净收入: {income}")
        if income >= INCOME_THRESHOLD:
            logger.info("净收入达标，进入雇佣研究助理")
            return "hire_assistant"
        else:
            logger.info(f"净收入不足{INCOME_THRESHOLD}，等待...")
            time.sleep(5)
            return None