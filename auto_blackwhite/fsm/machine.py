# 状态机主类（加载状态、执行迁移）

import time
import logging
from fsm.context import GameContext
from fsm.states import (
    StartState, SelectTalentState, TimeAllocateState,
    CheckPlanQueueState, SelfImproveState, SwitchToWorkState,
    CheckIncomeState, HireAssistantState, CheckPositionState,
    BuyCarAndUpgradeState, WaitSettlementState
)

logger = logging.getLogger("GameBot")

class GameStateMachine:
    def __init__(self, controller, recognizer):
        self.controller = controller
        self.recognizer = recognizer
        self.context = GameContext()
        # 注册所有状态
        self.states = {
            "start": StartState(),
            "select_talent": SelectTalentState(),
            "time_allocate": TimeAllocateState(),
            "check_plan_queue": CheckPlanQueueState(),
            "self_improve": SelfImproveState(),
            "switch_to_work": SwitchToWorkState(),
            "check_income": CheckIncomeState(),
            "hire_assistant": HireAssistantState(),
            "check_position": CheckPositionState(),
            "buy_car_and_upgrade": BuyCarAndUpgradeState(),
            "wait_settlement": WaitSettlementState(),
        }
        self.current_state_name = "start"
        self.running = True
    
    def transition_to(self, new_state_name):
        if new_state_name and new_state_name in self.states:
            logger.info(f"状态迁移: {self.current_state_name} -> {new_state_name}")
            self.states[self.current_state_name].on_exit(self.context)
            self.current_state_name = new_state_name
            self.states[self.current_state_name].on_enter(self.context)
        elif new_state_name is None:
            # 停留当前状态，不迁移
            pass
        else:
            logger.error(f"未知状态名: {new_state_name}")
    
    def run(self):
        # 进入初始状态
        self.states[self.current_state_name].on_enter(self.context)
        while self.running:
            current_state = self.states[self.current_state_name]
            next_state = current_state.execute(self.context, self.controller, self.recognizer)
            if next_state:
                self.transition_to(next_state)
            # 每次循环间隔较短，提高响应
            time.sleep(0.5)