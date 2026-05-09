# UI Automator Restart for handling UI Automator restart operations in the application

import logging
logger = logging.getLogger("GameBot")

class RestartUIAutomator:
    def __init__(self, controller):
        self.controller = controller
    
    def execute(self):
        logger.info("重启 uiautomator 服务")
        # 通过 ADB 重启 uiautomator 进程
        self.controller.connector.device.app_stop("com.github.uiautomator")
        # 等待重新初始化
        import time
        time.sleep(2)
        self.controller.connector.ensure_connected()