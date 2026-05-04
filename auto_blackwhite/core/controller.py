# 基础操作（点击、滑动、截图、OCR）
# core/controller.py
import time
import logging
import threading
from core.connector import DeviceConnector

logger = logging.getLogger("GameBot")

class GameController:
    def __init__(self, connector):
        self.connector = connector
        self.device = connector.device
        self.lock = threading.Lock()
    
    def safe_click(self, x, y, retry=3):
        with self.lock:
            """带重试的点击"""
        for i in range(retry):
            try:
                self.connector.ensure_connected()
                self.device.click(x, y)
                logger.debug(f"点击 ({x}, {y})")
                return True
            except Exception as e:
                logger.warning(f"点击失败 ({i+1}/{retry}): {e}")
                time.sleep(1)
        return False
    
    def safe_swipe(self, fx, fy, tx, ty, duration=0.5):
        with self.lock:
            """滑动"""
        try:
            self.connector.ensure_connected()
            self.device.swipe(fx, fy, tx, ty, duration=duration)
            logger.debug(f"滑动 ({fx},{fy}) -> ({tx},{ty})")
            return True
        except Exception as e:
            logger.error(f"滑动失败: {e}")
            return False
    
    def screenshot(self):
        with self.lock:
            """截图，返回PIL Image"""
        self.connector.ensure_connected()
        return self.device.screenshot()
    
    def get_pixel_color(self, x, y):
        with self.lock:
            """获取指定坐标像素颜色(RGB)"""
        img = self.screenshot()
        return img.getpixel((x, y))
    
    def press_back(self):
        with self.lock:
            """按返回键"""
        self.device.press("back")
        time.sleep(0.3)