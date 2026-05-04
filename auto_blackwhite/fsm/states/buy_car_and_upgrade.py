# 买防弹专用车+时间分配研究加号
# fsm/states/buy_car_and_upgrade.py
import time
from fsm.state import State
from config.settings import TRAFFIC_BUTTON, SCROLL_START, SCROLL_END, CAR_BUTTON_TEMPLATE, TIME_ALLOC_BUTTON, RESEARCH_PLUS_BUTTON
import logging
logger = logging.getLogger("GameBot")

class BuyCarAndUpgradeState(State):
    def execute(self, context, controller, recognizer):
        # 点击生活->交通
        # 以下为步骤框架
        logger.info("购买防弹专用车并增加研究时间")
        # TODO: 进入交通界面，滚动查找“防弹专用车”并点击
        # 使用滑动找图的方式
        # 没有实现模板匹配，简单假设直接点击固定坐标
        controller.safe_click(*TRAFFIC_BUTTON)
        time.sleep(1)
        # 滑动滚动，直到找到按钮（这里简化，直接点击某个坐标）
        # 点击防弹专用车
        # 完成后关闭界面
        # 回到主界面，打开时间分配，点击研究加号点满
        controller.safe_click(*TIME_ALLOC_BUTTON)
        time.sleep(0.5)
        for _ in range(20):  # 最大点击
            controller.safe_click(*RESEARCH_PLUS_BUTTON)
            time.sleep(0.1)
        controller.press_back()
        time.sleep(0.5)
        # 返回职位检查状态
        return "check_position"