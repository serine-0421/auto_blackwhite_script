# 任务基类

from abc import ABC, abstractmethod
import threading
import logging

logger = logging.getLogger("GameBot")

class BaseTask(ABC):
    """所有后台任务（如提神、看门狗）的基类"""
    
    def __init__(self, controller, recognizer, interval_seconds=10):
        self.controller = controller
        self.recognizer = recognizer
        self.interval = interval_seconds
        self.running = False
        self.thread = None
        self.lock = threading.Lock()   # 用于与主状态机共享资源
        self.name = self.__class__.__name__
    
    @abstractmethod
    def execute_once(self):
        """单次任务执行逻辑，子类必须实现"""
        pass
    
    def run_loop(self):
        """循环运行任务"""
        while self.running:
            try:
                with self.lock:
                    self.execute_once()
            except Exception as e:
                logger.error(f"{self.name} 执行出错: {e}")
            # 等待间隔
            import time
            time.sleep(self.interval)
    
    def start(self):
        """启动任务线程"""
        if self.running:
            logger.warning(f"{self.name} 已在运行")
            return
        self.running = True
        self.thread = threading.Thread(target=self.run_loop, daemon=True)
        self.thread.start()
        logger.info(f"{self.name} 已启动，间隔 {self.interval} 秒")
    
    def stop(self):
        """停止任务"""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)
        logger.info(f"{self.name} 已停止")