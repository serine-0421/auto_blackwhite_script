# 保存/加载当前状态机状态（用于重启恢复）

import json
import os
from typing import Optional
from fsm.enums.states import StateType
from fsm.context import GameContext
import logging

logger = logging.getLogger("GameBot")

class StatePersistence:
    """状态持久化，用于保存和加载状态机进度"""
    
    def __init__(self, save_file="data/state_save.json"):
        self.save_file = save_file
        # 确保目录存在
        os.makedirs(os.path.dirname(save_file), exist_ok=True)
    
    def save(self, state_type: StateType, context: GameContext):
        """保存当前状态和上下文"""
        data = {
            "state": state_type.name,
            "context": {
                "research_level": context.research_level,
                "net_income": context.net_income,
                "current_position": context.current_position,
                "position_level": context.position_level,
                "expenditure": context.expenditure,
                "retry_count": context.retry_count,
                "talent_selected": context.talent_selected,
                "last_state": context.last_state.name if context.last_state else None,
            }
        }
        with open(self.save_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"状态已保存: {state_type.name}")
    
    def load(self) -> tuple[Optional[StateType], Optional[GameContext]]:
        """加载保存的状态和上下文，返回 (StateType, GameContext) 或 (None, None)"""
        if not os.path.exists(self.save_file):
            logger.info("未找到保存文件，从头开始")
            return None, None
        try:
            with open(self.save_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            state_name = data.get("state")
            if not state_name:
                return None, None
            state_type = StateType[state_name]
            ctx_data = data.get("context", {})
            context = GameContext()
            context.research_level = ctx_data.get("research_level", 0)
            context.net_income = ctx_data.get("net_income", 0)
            context.current_position = ctx_data.get("current_position")
            context.position_level = ctx_data.get("position_level", 0)
            context.expenditure = ctx_data.get("expenditure", 0)
            context.retry_count = ctx_data.get("retry_count", 0)
            context.talent_selected = ctx_data.get("talent_selected", 0)
            last_state_name = ctx_data.get("last_state")
            if last_state_name:
                context.last_state = StateType[last_state_name]
            logger.info(f"加载保存状态: {state_name}")
            return state_type, context
        except Exception as e:
            logger.error(f"加载保存文件失败: {e}")
            return None, None
    
    def clear(self):
        """清除保存文件"""
        if os.path.exists(self.save_file):
            os.remove(self.save_file)
            logger.info("已清除保存的状态文件")