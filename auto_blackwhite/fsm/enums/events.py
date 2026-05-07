# 事件枚举

from enum import Enum, auto

class EventType(Enum):
    # 由状态返回值触发的事件
    NEXT = auto()           # 进入下一个预设状态
    RETRY = auto()          # 重试当前状态
    ERROR = auto()          # 发生错误，进入恢复状态
    RECONNECT = auto()      # 需要重连设备
    STOP = auto()           # 停止运行