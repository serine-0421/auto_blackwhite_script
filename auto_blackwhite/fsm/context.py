# 上下文（共享数据：当前等级、净收入、职位等）

class GameContext:
    def __init__(self):
        self.research_level = 0       # 活力研究等级
        self.research_level_ts = 0    # 最近一次识别活力研究等级的时间戳
        self.energy_level = 0
        self.net_income = 0           # 净收入
        self.current_position = None  # 职位字符串
        self.position_level = 0       # 职位等级（仅研究主任需要）
        self.expenditure = 0          # 雇佣后的支出
        self.retry_count = 0          # 当前状态重试计数
        self.talent_selected = 0      # 已选天赋次数
        self.last_state = None        # 上一个状态类型（用于恢复）
    
    def update_from_ocr(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                if key == 'research_level':
                    try:
                        import time
                        self.research_level_ts = time.time()
                    except Exception:
                        self.research_level_ts = 0