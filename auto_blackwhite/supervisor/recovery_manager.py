# Recovery Manager for handling recovery operations in the application

import logging
from supervisor.recovery import (
    ReconnectADB, RestartUIAutomator, RestartEmulator, RestartFSM
)

logger = logging.getLogger("GameBot")

class RecoveryManager:
    def __init__(self, controller, state_machine, task_scheduler):
        self.controller = controller
        self.state_machine = state_machine
        self.task_scheduler = task_scheduler
        self.recovery_map = {
            "reconnect_adb": ReconnectADB(controller),
            "restart_uiautomator": RestartUIAutomator(controller),
            "restart_emulator": RestartEmulator(controller),
            "restart_fsm": RestartFSM(state_machine)
        }
    
    def recover(self, action_name):
        logger.info(f"执行恢复操作: {action_name}")
        recovery = self.recovery_map.get(action_name)
        if recovery:
            recovery.execute()
        else:
            logger.error(f"未知恢复操作: {action_name}")