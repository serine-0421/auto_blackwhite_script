# 状态基类（每个状态一个类实例）

from abc import ABC, abstractmethod
from fsm.enums.results import StateResult
from fsm.enums.events import EventType
import logging

logger = logging.getLogger("GameBot")

class State(ABC):
    """状态基类"""
    
    @abstractmethod
    def execute(self, context, controller, recognizer):
        """
        执行状态逻辑。
        返回 (StateResult, next_state_type or event, data)
        - StateResult: 执行结果枚举
        - next: 如果 StateResult.SUCCESS，则为下一个 StateType；若为 StateResult.ERROR，则为 EventType 或其他
        - data: 可选附加数据
        """
        pass
    
    def on_enter(self, context):
        logger.info(f"进入状态: {self.__class__.__name__}")
    
    def on_exit(self, context):
        logger.info(f"退出状态: {self.__class__.__name__}")# fsm/state.py
from abc import ABC, abstractmethod
from fsm.enums.results import StateResult
from fsm.enums.events import EventType
import logging

logger = logging.getLogger("GameBot")

class State(ABC):
    """状态基类"""
    
    @abstractmethod
    def execute(self, context, controller, recognizer):
        """
        执行状态逻辑。
        返回 (StateResult, next_state_type or event, data)
        - StateResult: 执行结果枚举
        - next: 如果 StateResult.SUCCESS，则为下一个 StateType；若为 StateResult.ERROR，则为 EventType 或其他
        - data: 可选附加数据
        """
        pass
    
    def on_enter(self, context):
        logger.info(f"进入状态: {self.__class__.__name__}")
    
    def on_exit(self, context):
        logger.info(f"退出状态: {self.__class__.__name__}")