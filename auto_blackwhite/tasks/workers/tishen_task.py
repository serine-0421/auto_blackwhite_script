# 提神独立任务（独立线程或主循环轮询）

import time
import logging
from tasks.base.base_task import BaseTask
from config.settings import TISHEN_CHECK_INTERVAL, TISHEN_CIRCLE_REGION, TISHEN_CIRCLE_CLICK, TISHEN_OPTIONS

logger = logging.getLogger("GameBot")

class TishenTask(BaseTask):
    """独立提神任务，周期性检测并执行提神"""
    def __init__(self, controller, recognizer, lock):
        super().__init__(controller, recognizer, lock)
        self.interval = TISHEN_CHECK_INTERVAL   # 10秒
    
    def execute(self):
        # 识别圆圈数字
        num = self.recognizer.ocr_number(TISHEN_CIRCLE_REGION)
        if num is None or not isinstance(num, int) or num <= 0:
            logger.debug("提神次数为0或识别失败，跳过")
            return

        logger.info(f"发现提神次数: {num}")
        # 点击圆圈
        self.controller.safe_click(*TISHEN_CIRCLE_CLICK)
        time.sleep(0.5)
        # 点击前两个提神选项
        for pos in TISHEN_OPTIONS:
            self.controller.safe_click(*pos)
            time.sleep(0.3)
        # 提神完成后，按返回键回到主界面（可能需要多次）
        for _ in range(3):
            self.controller.press_back()
            time.sleep(0.3)
