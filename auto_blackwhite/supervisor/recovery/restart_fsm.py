# FSM Restart for handling FSM restart operations in the application

import logging
logger = logging.getLogger("GameBot")

class RestartFSM:
    def __init__(self, state_machine):
        self.state_machine = state_machine
    
    def execute(self):
        logger.info("重启状态机 - 重置到初始状态")
        if self.state_machine:
            self.state_machine.current_state_type = self.state_machine.context.last_state or "start"
            # 强制重新进入状态