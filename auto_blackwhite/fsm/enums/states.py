# 状态枚举

from enum import Enum, auto

class StateType(Enum):
    # startup 组
    START = auto()
    SELECT_TALENT = auto()
    TIME_ALLOCATE = auto()
    
    # growth 组
    SELF_IMPROVE = auto()
    CHECK_INCOME = auto()
    HIRE_ASSISTANT = auto()
    
    # progression 组
    CHECK_POSITION = auto()
    BUY_CAR_AND_UPGRADE = auto()
    WAIT_SETTLEMENT = auto()
    
    # system 组
    RECOVERY = auto()
    RECONNECT = auto()
    WATCHDOG = auto()