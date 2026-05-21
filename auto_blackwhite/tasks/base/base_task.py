# 任务基类

import threading
import logging

logger = logging.getLogger("GameBot")

class BaseTask:
    """
    任务基类，所有 worker 任务继承此类。
    每个任务运行在独立线程中，需要与主状态机共享 controller 锁。
    """
    def __init__(self, controller, recognizer, lock):
        self.controller = controller
        self.recognizer = recognizer
        self.lock = lock          # 与状态机共享的锁，避免UI操作冲突
        self.running = True
        self.interval = 0         # 子类应覆盖此值，单位秒
    
    def run_loop(self):
        """任务主循环，在线程中执行

        注意：Controller 自带锁保护每次 UI 操作，因此不应在整个 execute 期间持有锁。
        否则会导致后台任务占用锁并阻塞主状态机，造成提神线程与主循环不兼容。
        """
        logger.info(f"启动任务: {self.__class__.__name__}")
        while self.running:
            try:
                self.execute()
            except Exception as e:
                logger.exception(f"任务 {self.__class__.__name__} 执行异常: {e}")
            # 等待间隔
            import time
            time.sleep(self.interval)
    
    def execute(self):
        """子类实现具体逻辑"""
        raise NotImplementedError
    
    def stop(self):
        self.running = False