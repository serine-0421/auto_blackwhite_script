# Auto Save Task for handling automatic saving of game progress in the application

import time
import logging
from tasks.base.base_task import BaseTask
from persistence.state_persistence import StatePersistence

logger = logging.getLogger("GameBot")

class AutoSaveTask(BaseTask):
    """定期保存状态机进度"""
    def __init__(self, controller, recognizer, lock, state_machine):
        super().__init__(controller, recognizer, lock)
        self.interval = 300   # 每5分钟保存一次
        self.state_machine = state_machine
        self.persistence = StatePersistence()
    
    def execute(self):
        try:
            state = self.state_machine.current_state_type.name if self.state_machine else None
            context = self.state_machine.context if self.state_machine else None
            self.persistence.save_state(state, context)
            logger.debug("状态已自动保存")
        except Exception as e:
            logger.error(f"自动保存失败: {e}")