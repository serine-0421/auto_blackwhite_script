# 状态工厂

from fsm.enums.states import StateType
from fsm.state import State
from fsm.states.startup.start import StartState
from fsm.states.startup.select_talent import SelectTalentState
from fsm.states.startup.time_allocate import TimeAllocateState
from fsm.states.growth.self_improve import SelfImproveState
from fsm.states.growth.check_income import CheckIncomeState
from fsm.states.growth.hire_assistant import HireAssistantState
from fsm.states.progression.check_position import CheckPositionState
from fsm.states.progression.buy_car_and_upgrade import BuyCarAndUpgradeState
from fsm.states.progression.wait_settlement import WaitSettlementState
from fsm.states.system.recovery import RecoveryState
from fsm.states.system.reconnect import ReconnectState
from fsm.states.system.watchdog import WatchdogState

class StateFactory:
    @staticmethod
    def create(state_type: StateType) -> State:
        mapping = {
            StateType.START: StartState,
            StateType.SELECT_TALENT: SelectTalentState,
            StateType.TIME_ALLOCATE: TimeAllocateState,
            StateType.SELF_IMPROVE: SelfImproveState,
            StateType.CHECK_INCOME: CheckIncomeState,
            StateType.HIRE_ASSISTANT: HireAssistantState,
            StateType.CHECK_POSITION: CheckPositionState,
            StateType.BUY_CAR_AND_UPGRADE: BuyCarAndUpgradeState,
            StateType.WAIT_SETTLEMENT: WaitSettlementState,
            StateType.RECOVERY: RecoveryState,
            StateType.RECONNECT: ReconnectState,
            StateType.WATCHDOG: WatchdogState,
        }
        state_class = mapping.get(state_type)
        if not state_class:
            raise ValueError(f"未知状态类型: {state_type}")
        return state_class()