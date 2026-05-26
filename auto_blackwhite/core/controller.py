# 基础操作（点击、滑动、截图、OCR）

import time
import logging
import threading

logger = logging.getLogger("GameBot")


class GameController:
    def __init__(self, connector):
        self.connector = connector
        self.lock = threading.RLock()

    # 内部工具

    def _safe_exec(self, fn, name, retry=3, delay=0.5):
        """统一执行框架（核心升级点）"""
        for i in range(retry):
            try:
                device = self.connector.ensure_connected()
                with self.lock:
                    return fn(device)
            except Exception as e:
                logger.warning(f"[{name}] failed {i+1}/{retry}: {e}")
                time.sleep(delay * (i + 1))  # exponential backoff
        return None

    # 操作层

    def click(self, x, y, retry=3):
        logger.info(f"准备点击 ({x}, {y})")
        def _(device):
            device.click(x, y)
            logger.info(f"点击成功 ({x}, {y})")
            logger.debug(f"click ({x}, {y})")
            time.sleep(0.5)
            return True

        result = self._safe_exec(_, "click", retry)
        if not result:
            logger.warning(f"点击失败 ({x}, {y})")
        return result

    def swipe(self, fx, fy, tx, ty, duration=0.5, retry=2):
        logger.info(f"准备滑动 ({fx},{fy}) -> ({tx},{ty})")
        def _(device):
            device.swipe(fx, fy, tx, ty, duration=duration)
            logger.info(f"滑动成功 ({fx},{fy}) -> ({tx},{ty})")
            logger.debug(f"swipe ({fx},{fy}) -> ({tx},{ty})")
            return True

        result = self._safe_exec(_, "swipe", retry)
        if not result:
            logger.warning(f"滑动失败 ({fx},{fy}) -> ({tx},{ty})")
        return result

    def safe_click(self, x, y, retry=3):
        return self.click(x, y, retry)

    def press_back(self):
        logger.info("准备按返回键")
        def _(device):
            device.press("back")
            time.sleep(0.5)
            return True

        result = self._safe_exec(_, "back", retry=1)
        if result:
            logger.info("返回键执行成功")
        else:
            logger.warning("返回键执行失败")
        return result

    # 视觉相关（待完善）

    def screenshot(self):
        def _(device):
            return device.screenshot()

        return self._safe_exec(_, "screenshot", retry=1)

    def get_pixel_color(self, x, y):
        img = self.screenshot()
        if img is None:
            return None
        return img.getpixel((x, y))