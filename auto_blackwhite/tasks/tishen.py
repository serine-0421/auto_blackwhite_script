# 提神独立任务（独立线程或主循环轮询）
# tasks/tishen.py
import time
import threading
import logging
from config.settings import TISHEN_CHECK_INTERVAL, TISHEN_CIRCLE_REGION, TISHEN_CIRCLE_CLICK, TISHEN_OPTIONS

logger = logging.getLogger("GameBot")

class TishenTask:
    def __init__(self, controller, recognizer):
        self.controller = controller
        self.recognizer = recognizer
        self.lock = threading.Lock()
        self.running = True
    
    def run_loop(self):
        """每隔 TISHEN_CHECK_INTERVAL 秒检查一次提神"""
        while self.running:
            try:
                with self.lock:
                    self._check_and_tishen()
            except Exception as e:
                logger.error(f"提神检查出错: {e}")
            time.sleep(TISHEN_CHECK_INTERVAL)
    
    def _check_and_tishen(self):
        # 识别圆圈数字
        num = self.recognizer.ocr_number(TISHEN_CIRCLE_REGION)
        if num > 0:
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
        else:
            logger.debug(f"提神次数为0，跳过")