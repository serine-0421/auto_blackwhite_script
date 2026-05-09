# ADB Reconnect for handling ADB connection recovery in the application

import logging
logger = logging.getLogger("GameBot")

class ReconnectADB:
    def __init__(self, controller):
        self.controller = controller
    
    def execute(self):
        logger.info("执行 ADB 重连")
        self.controller.connector.ensure_connected()