# 基础操作（点击、滑动、截图、OCR）

import time
import logging
import threading

logger = logging.getLogger("GameBot")


class GameController:
    def __init__(self, connector):
        self.connector = connector
        self.device = connector.device
        self.lock = threading.RLock() 

    # 内部工具

    def _safe_exec(self, fn, name, retry=3, delay=0.5):
        """统一执行框架（核心升级点）"""
        for i in range(retry):
            try:
                self.connector.ensure_connected()
                with self.lock:
                    return fn()
            except Exception as e:
                logger.warning(f"[{name}] failed {i+1}/{retry}: {e}")
                time.sleep(delay * (i + 1))  # exponential backoff
        return None

    # 操作层

    def click(self, x, y, retry=3):
        def _():
            self.device.click(x, y)
            logger.debug(f"click ({x}, {y})")
            return True

        return self._safe_exec(_, "click", retry)

    def swipe(self, fx, fy, tx, ty, duration=0.5, retry=2):
        def _():
            self.device.swipe(fx, fy, tx, ty, duration=duration)
            logger.debug(f"swipe ({fx},{fy}) -> ({tx},{ty})")
            return True

        return self._safe_exec(_, "swipe", retry)

    def press_back(self):
        def _():
            self.device.press("back")
            time.sleep(0.2)
            return True

        return self._safe_exec(_, "back", retry=1)

    # 视觉相关（待完善）

    def screenshot(self):
        def _():
            return self.device.screenshot()

        return self._safe_exec(_, "screenshot", retry=1)

    def get_pixel_color(self, x, y):
        img = self.screenshot()
        if img is None:
            return None
        return img.getpixel((x, y))