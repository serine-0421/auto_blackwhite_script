# 提神独立任务（独立线程或主循环轮询）

import time
import logging
from tasks.base_task import BaseTask
from config.settings import TISHEN_CIRCLE_REGION, TISHEN_CIRCLE_CLICK, TISHEN_OPTIONS

logger = logging.getLogger("GameBot")

class TishenTask(BaseTask):
    def __init__(self, controller, recognizer, interval_seconds=10):
        super().__init__(controller, recognizer, interval_seconds)
    
    def execute_once(self):
        # 识别圆圈数字
        num = self.recognizer.ocr_number(TISHEN_CIRCLE_REGION)
        if num > 0:
            logger.info(f"发现提神次数: {num}")
            with self.lock:
                self.controller.safe_click(*TISHEN_CIRCLE_CLICK)
                time.sleep(0.5)
                for pos in TISHEN_OPTIONS:
                    self.controller.safe_click(*pos)
                    time.sleep(0.3)
                for _ in range(3):
                    self.controller.press_back()
                    time.sleep(0.3)
        else:
            logger.debug(f"提神次数为0，跳过")