# 设备连接管理（u2、ADB重连）
# core/connector.py
import uiautomator2 as u2
import time
import logging

logger = logging.getLogger("GameBot")

class DeviceConnector:
    def __init__(self, addr):
        self.addr = addr
        self.device = None
        self.connect()
    
    def connect(self):
        """连接设备，如果失败则重试"""
        while True:
            try:
                self.device = u2.connect(self.addr)
                # 测试连接
                self.device.info
                logger.info(f"设备连接成功: {self.addr}")
                return self.device
            except Exception as e:
                logger.error(f"连接失败: {e}, 5秒后重试...")
                time.sleep(5)
    
    def ensure_connected(self):
        """确保连接有效，否则重连"""
        try:
            self.device.info
            return True
        except:
            logger.warning("设备连接断开，尝试重连...")
            self.connect()
            return True