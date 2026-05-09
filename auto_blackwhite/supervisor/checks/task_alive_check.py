# Task Alive Check for validating task status in the application

class TaskAliveCheck:
    def __init__(self, task_scheduler):
        self.task_scheduler = task_scheduler
    
    def passed(self):
        # 检查各任务线程是否还活着
        for t in self.task_scheduler.threads:
            if not t.is_alive():
                return False
        return True
    
    def get_recovery_action(self):
        return "restart_fsm"