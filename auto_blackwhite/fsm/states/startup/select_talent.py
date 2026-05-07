# 选天赋（3次点击固定位置）
# fsm/states/select_talent.py
import time
from fsm.state import State
from config.settings import TALENT_POSITIONS, TALENT_SELECT_COUNT
import logging
logger = logging.getLogger("GameBot")

class SelectTalentState(State):
    def execute(self, context, controller, recognizer):
        # 随机点击天赋点（ABCD任意）
        # 由于必须点3次，每次点一个位置，重复3次
        # 这里假设3次点的位置不同，但游戏可能自动刷新新的一排，简单处理：连续点击同一个位置也可以
        for i in range(TALENT_SELECT_COUNT):
            # 随便选一个位置，这里取第一个
            x, y = TALENT_POSITIONS[0]
            controller.safe_click(x, y)
            time.sleep(0.5)
        context.talent_selected = TALENT_SELECT_COUNT
        logger.info("天赋选择完成")
        return "time_allocate"