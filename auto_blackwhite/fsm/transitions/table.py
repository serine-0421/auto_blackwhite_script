# 状态迁移表

from fsm.enums.states import StateType

# 定义状态迁移规则：每个状态执行成功后的下一个状态
TRANSITION_TABLE = {
    StateType.START: StateType.SELECT_TALENT,
    StateType.SELECT_TALENT: StateType.TIME_ALLOCATE,
    StateType.TIME_ALLOCATE: StateType.SELF_IMPROVE,
    StateType.SELF_IMPROVE: StateType.CHECK_INCOME,     # 注意：实际流程中 self_improve 成功后应先去工作界面再检查收入，但为了简化先直接指向CHECK_INCOME，细节在状态内部调整
    StateType.CHECK_INCOME: StateType.HIRE_ASSISTANT,   # 收入达标后进入雇佣
    StateType.HIRE_ASSISTANT: StateType.CHECK_POSITION,
    StateType.CHECK_POSITION: StateType.WAIT_SETTLEMENT,  # 满足结束条件
    StateType.BUY_CAR_AND_UPGRADE: StateType.CHECK_POSITION,  # 买车后重回职位检查
    StateType.WAIT_SETTLEMENT: StateType.START,          # 结算后重新开始
    # 系统状态迁移
    StateType.RECOVERY: StateType.START,                 # 恢复后重新开始
    StateType.RECONNECT: StateType.START,
    StateType.WATCHDOG: StateType.START,
}

# 失败/重试时的默认目标（一般停留或回到上一个）
RETRY_TARGET = None       # None 表示停留在当前状态重试
ERROR_TARGET = StateType.RECOVERY