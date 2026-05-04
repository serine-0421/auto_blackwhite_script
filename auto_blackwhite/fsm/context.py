# 上下文（共享数据：当前等级、净收入、职位等）
# fsm/context.py
class GameContext:
    def __init__(self):
        self.research_level = 0       # 活力研究等级
        self.net_income = 0           # 净收入
        self.current_position = None  # 职位字符串
        self.position_level = 0       # 职位等级（仅研究主任需要）
        self.expenditure = 0          # 雇佣后的支出
        self.retry_count = 0          # 重试计数
        self.talent_selected = 0      # 已选天赋次数
        # 可根据需要增加字段
    
    def update_from_ocr(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)