 # 检查职位（研究生/研究员/...）及等级
# fsm/states/check_position.py
import time
from fsm.state import State
from config.settings import POSITION_REGION, DIRECTOR_LEVEL_THRESHOLD
import logging
logger = logging.getLogger("GameBot")

class CheckPositionState(State):
    def execute(self, context, controller, recognizer):
        # 确保在工作-科研界面，识别职位文字
        pos = recognizer.ocr_position_text(POSITION_REGION)
        if pos is None:
            logger.warning("识别职位失败，等待重试")
            time.sleep(2)
            return None
        context.current_position = pos
        logger.info(f"当前职位: {pos}")
        # 根据用户规则
        if pos in ["研究生", "研究员", "资深研究员", "课题组长"]:
            # 等待循环（停留在本状态，但需要定期检测是否变化）
            logger.info("职位未达研究主任，等待")
            time.sleep(10)
            return None
        elif pos == "研究主任":
            # 需要判断等级
            # 等级可能需要从其他地方OCR，假设上下文中有position_level
            # 这里简单模拟：调用OCR识别等级数字（位置未知，暂用占位）
            level = -1
            # TODO: 实现等级识别 (比如在职位旁边有数字)
            # 暂时假设通过某种方式获取
            if level >= DIRECTOR_LEVEL_THRESHOLD:
                logger.info(f"研究主任等级>=10，等待游戏结束")
                # 等待结算
                return "wait_settlement"
            else:
                logger.info(f"研究主任等级{level}<10，需要买车升级")
                return "buy_car_and_upgrade"
        else:
            # 按照用户说明，case else 同研究主任等级>=10一样执行（等待结算）
            logger.info(f"未知职位或特殊情况: {pos}，当作等待结算")
            return "wait_settlement"