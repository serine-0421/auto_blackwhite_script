# 结果枚举

from enum import Enum, auto

class StateResult(Enum):
    SUCCESS = auto()        # 状态执行成功，可迁移
    FAILURE = auto()        # 状态执行失败（可重试）
    WAITING = auto()        # 等待条件满足，停留
    ERROR = auto()          # 严重错误，需要特殊处理