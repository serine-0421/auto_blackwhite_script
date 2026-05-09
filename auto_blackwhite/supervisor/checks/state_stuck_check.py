# State Stuck Check for validating application state in the application

import time
class StateStuckCheck:
    def __init__(self, state_machine, timeout=300):
        self.state_machine = state_machine
        self.timeout = timeout
        self.last_state = None
        self.last_change_time = time.time()
    
    def passed(self):
        current_state = self.state_machine.current_state_type if self.state_machine else None
        if current_state != self.last_state:
            self.last_state = current_state
            self.last_change_time = time.time()
            return True
        # 同一状态停留超时，认为卡死
        if time.time() - self.last_change_time > self.timeout:
            return False
        return True
    
    def get_recovery_action(self):
        return "restart_fsm"