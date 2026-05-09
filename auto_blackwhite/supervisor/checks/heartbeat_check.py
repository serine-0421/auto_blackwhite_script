# Heartbeat Check for validating application heartbeat in the application

import time
class HeartbeatCheck:
    def __init__(self, controller):
        self.controller = controller
        self.last_heartbeat = time.time()
    
    def passed(self):
        # 检查主循环或某个心跳变量是否更新
        # 简单实现：检查时间差，如果超过阈值则失败
        if time.time() - self.last_heartbeat > 60:
            return False
        return True
    
    def heartbeat(self):
        self.last_heartbeat = time.time()
    
    def get_recovery_action(self):
        return "restart_fsm"