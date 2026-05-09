# 监控模拟器/ADB连接是否存活

import threading
import time
import logging
from supervisor.recovery_manager import RecoveryManager
from supervisor.checks import (
    ADBCheck, EmulatorCheck, HeartbeatCheck,
    StateStuckCheck, TaskAliveCheck
)

logger = logging.getLogger("GameBot")

class Watchdog:
    """看门狗：周期性执行各项检查，发现问题则触发恢复"""
    def __init__(self, controller, state_machine, task_scheduler):
        self.controller = controller
        self.state_machine = state_machine
        self.task_scheduler = task_scheduler
        self.recovery_manager = RecoveryManager(controller, state_machine, task_scheduler)
        self.checks = [
            ADBCheck(controller),
            EmulatorCheck(controller),
            HeartbeatCheck(controller),
            StateStuckCheck(state_machine),
            TaskAliveCheck(task_scheduler)
        ]
        self.running = True
        self.interval = 30  
    
    def start(self):
        t = threading.Thread(target=self._run, daemon=True)
        t.start()
        logger.info("Watchdog 已启动")
    
    def _run(self):
        while self.running:
            try:
                for check in self.checks:
                    if not check.passed():
                        logger.warning(f"检查失败: {check.__class__.__name__}")
                        self.recovery_manager.recover(check.get_recovery_action())
                        break  
            except Exception as e:
                logger.exception(f"Watchdog 异常: {e}")
            time.sleep(self.interval)
    
    def stop(self):
        self.running = False