# 自我提升-活力研究（循环检测等级<150）

import time
from fsm.state import State
from config.settings import LIFE_BUTTON, YANJIU_BUTTON, SELF_IMPROVE_BUTTON, VITALITY_RESEARCH_REGION, VITALITY_TARGET_LEVEL
import logging
TARGET_ENERGY = 150
logger = logging.getLogger("GameBot")

class SelfImproveState(State):
    def execute(self, context, controller, recognizer):
        # 先检查 context
        if context.energy_level >= TARGET_ENERGY:
            logger.info("活力等级已达标，跳过SelfImproveState")
            return "switch_to_work"

        # 如果最近已经识别过活力研究等级（TTL 5 分钟），使用缓存避免重复识别
        RECACHE_TTL = 300
        if getattr(context, 'research_level_ts', 0) and (time.time() - context.research_level_ts) < RECACHE_TTL:
            level = context.research_level
            logger.info(f"使用缓存的活力研究等级: {level} (上次识别{int(time.time()-context.research_level_ts)}秒前)")
            if level >= VITALITY_TARGET_LEVEL:
                logger.info("缓存等级达标，跳过识别并进入下一状态")
                return "switch_to_work"
            else:
                logger.info("缓存等级未达标，继续进入自我提升界面进行分配")

        if getattr(context, 'vitality_research_ocr_failed', False):
            logger.warning("已达到活力研究等级识别失败阈值，跳过后续识别")
            return "switch_to_work"

        # 进入自我提升界面并读取活力研究等级
        controller.safe_click(*SELF_IMPROVE_BUTTON)
        time.sleep(1)
        # 循环读取活力研究等级
        max_attempts = 5
        attempts = 0
        while attempts < max_attempts:
            attempts += 1
            level = recognizer.ocr_number(VITALITY_RESEARCH_REGION)
            if level is None or level == -1:
                logger.warning(f"识别活力研究等级失败，重试 {attempts}/{max_attempts}")
                if attempts == 1:
                    logger.info("首次识别失败，依次点击 LIFE_BUTTON、YANJIU_BUTTON、SELF_IMPROVE_BUTTON 重新进入界面")
                    controller.safe_click(*LIFE_BUTTON)
                    time.sleep(0.5)
                    controller.safe_click(*YANJIU_BUTTON)
                    time.sleep(0.5)
                    controller.safe_click(*SELF_IMPROVE_BUTTON)
                    time.sleep(1)
                else:
                    time.sleep(3)
                continue
            # 使用 update_from_ocr 以便更新 context 中的时间戳
            if hasattr(context, 'update_from_ocr'):
                context.update_from_ocr(research_level=level)
            else:
                context.research_level = level
            logger.info(f"活力研究等级: {level}")
            if level >= VITALITY_TARGET_LEVEL:
                logger.info("活力研究等级达标，进入下一状态")
                # 返回主界面（按返回键）
                controller.press_back()
                time.sleep(0.5)
                return "switch_to_work"
            else:
                logger.info(f"等级不足{level}<150，等待3秒...")
                time.sleep(3)

        logger.warning(f"活力研究等级连续{max_attempts}次识别失败，自动进入下一流程")
        context.vitality_research_ocr_failed = True
        recognizer.save_debug_screenshot(
            VITALITY_RESEARCH_REGION,
            prefix="vitality_level_fail"
        )
        controller.press_back()
        time.sleep(0.5)
        context.click_research_student = True
        return "switch_to_work"
