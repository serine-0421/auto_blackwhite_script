# 状态基类（每个状态一个类实例）
# fsm/state.py
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger("GameBot")

class State(ABC):
    @abstractmethod
    def execute(self, context, controller, recognizer):
        """
        执行当前状态的逻辑。
        返回下一个状态的名称（字符串），如果返回None则停留在当前状态。
        """
        pass
    
    def on_enter(self, context):
        logger.info(f"进入状态: {self.__class__.__name__}")
    
    def on_exit(self, context):
        logger.info(f"退出状态: {self.__class__.__name__}")