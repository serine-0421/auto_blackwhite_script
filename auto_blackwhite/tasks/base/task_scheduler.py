# Task Scheduler for managing and executing tasks in the application

import threading
import logging
from tasks.base.task_registry import TaskRegistry

logger = logging.getLogger("GameBot")

class TaskScheduler:
    """调度器：为每个注册的任务创建并启动线程"""
    def __init__(self):
        self.threads = []
    
    def start_all(self):
        for task in TaskRegistry.get_all():
            t = threading.Thread(target=task.run_loop, daemon=True)
            t.start()
            self.threads.append(t)
            logger.info(f"任务线程已启动: {task.__class__.__name__}")
    
    def stop_all(self):
        for task in TaskRegistry.get_all():
            task.stop()
        for t in self.threads:
            t.join(timeout=2)