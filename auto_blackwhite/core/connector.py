# 设备连接管理（u2、ADB重连）

import time
import subprocess
import uiautomator2 as u2
import logging

logger = logging.getLogger("GameBot")


class DeviceConnector:
    def __init__(self, addr, max_retries=5, retry_interval=5):
        self.addr = addr
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.device = None

    def connect(self):
        """建立连接（带重试 + 失败抛异常）"""
        last_exception = None

        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(f"[Connector] 尝试连接设备 ({attempt}/{self.max_retries})")

                self.device = u2.connect(self.addr)

                # 健康检查
                _ = self.device.info

                logger.info(f"[Connector] 连接成功: {self.addr}")
                return self.device

            except Exception as e:
                last_exception = e
                logger.error(f"[Connector] 连接失败: {e}")

                # 尝试修复环境
                self._try_recover()

                time.sleep(self.retry_interval)

        raise RuntimeError(f"设备连接失败（已重试 {self.max_retries} 次）: {last_exception}")

    def ensure_connected(self):
        """确保设备可用（失败会抛异常）"""
        if self.device is None:
            return self.connect()

        try:
            _ = self.device.info
            return self.device

        except Exception as e:
            logger.warning(f"[Connector] 连接断开: {e}")
            return self.reconnect()

    def reconnect(self):
        """强制重连"""
        logger.warning("[Connector] 正在重连设备...")
        self.device = None
        return self.connect()

    def _try_recover(self):
        """尝试修复常见问题（adb / uiautomator2）"""
        logger.warning("[Connector] 尝试修复连接环境...")

        try:
            # 重启 adb
            subprocess.run("adb kill-server", shell=True)
            subprocess.run("adb start-server", shell=True)

            logger.info("[Connector] adb 已重启")

        except Exception as e:
            logger.error(f"[Connector] adb 重启失败: {e}")

        # 注意：这里不能保证 device 一定存在
        if self.device:
            try:
                self.device.service("uiautomator").start()
                logger.info("[Connector] uiautomator2 服务已重启")
            except Exception:
                pass