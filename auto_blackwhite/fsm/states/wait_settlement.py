# 等待结算画面，点击重新开始
# fsm/states/wait_settlement.py
import time
from fsm.state import State
from config.settings import SETTLEMENT_REGION, SETTLEMENT_CLICK_POS
import logging
logger = logging.getLogger("GameBot")

class WaitSettlementState(State):
    def execute(self, context, controller, recognizer):
        # 持续检测结算画面是否出现
        # 假设通过像素颜色变化判断，简单做法：等待固定时间
        # 更可靠：截图特定区域是否变成结算背景
        # 这里采用检测一个特征像素
        logger.info("等待结算画面...")
        # 示例：检测某个像素颜色是否改变
        # 暂用延时代替
        time.sleep(30)
        # 检测到结算后，点击任意位置重新开始
        controller.safe_click(*SETTLEMENT_CLICK_POS)
        time.sleep(2)
        logger.info("新一轮开始")
        return "start"