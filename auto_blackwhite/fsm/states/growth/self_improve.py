# 自我提升-活力研究（循环检测等级<150）
# fsm/states/self_improve.py
import time
from fsm.state import State
from config.settings import SELF_IMPROVE_BUTTON, VITALITY_RESEARCH_REGION, VITALITY_TARGET_LEVEL
import logging
logger = logging.getLogger("GameBot")

class SelfImproveState(State):
    def execute(self, context, controller, recognizer):
        # 进入自我提升界面
        controller.safe_click(*SELF_IMPROVE_BUTTON)
        time.sleep(1)
        # 循环读取活力研究等级
        while True:
            level = recognizer.ocr_number(VITALITY_RESEARCH_REGION)
            if level == -1:
                logger.warning("识别活力研究等级失败，重试")
                time.sleep(3)
                continue
            context.research_level = level
            logger.info(f"活力研究等级: {level}")
            if level >= VITALITY_TARGET_LEVEL:
                logger.info("活力研究等级达标，进入下一状态")
                # 返回主界面（按返回键）
                controller.press_back()
                time.sleep(0.5)
                return "switch_to_work"
            else:
                logger.info(f"等级不足{level}<150，等待3秒...")
                time.sleep(3)