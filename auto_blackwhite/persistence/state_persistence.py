# 保存/加载当前状态机状态（用于重启恢复）

import json
import os
import time
import logging
from typing import Optional

from fsm.enums.states import StateType
from fsm.context import GameContext

logger = logging.getLogger("GameBot")


class StatePersistence:
    """状态机运行时持久化"""

    SAVE_VERSION = 1

    def __init__(self, save_file: str = "data/state_save.json"):
        self.save_file = save_file

        save_dir = os.path.dirname(save_file)

        if save_dir:
            os.makedirs(save_dir, exist_ok=True)

    def save(self, state_type: StateType, context: GameContext):
        """保存状态机快照"""

        data = {
            "version": self.SAVE_VERSION,

            "saved_at": time.time(),

            "state": state_type.name,

            "context": context.to_dict()
        }

        tmp_file = f"{self.save_file}.tmp"

        try:
            with open(tmp_file, "w", encoding="utf-8") as f:
                json.dump(
                    data,
                    f,
                    indent=2,
                    ensure_ascii=False
                )

            # 原子替换
            os.replace(tmp_file, self.save_file)

            logger.info(
                f"状态保存成功: {state_type.name}"
            )

        except Exception:
            logger.exception("状态保存失败")

    def load(
        self
    ) -> tuple[Optional[StateType], Optional[GameContext]]:

        if not os.path.exists(self.save_file):
            logger.info("未发现状态存档")

            return None, None

        try:
            with open(
                self.save_file,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

            version = data.get("version", 0)

            if version != self.SAVE_VERSION:
                logger.warning(
                    f"存档版本不匹配: {version}"
                )

                return None, None

            state_name = data.get("state")

            if not state_name:
                raise ValueError("缺少 state 字段")

            state_type = StateType[state_name]

            context_data = data.get("context", {})

            context = GameContext.from_dict(context_data)

            saved_at = data.get("saved_at", 0)

            offline_seconds = int(
                time.time() - saved_at
            )

            logger.info(
                f"状态恢复成功: {state_name} "
                f"(离线 {offline_seconds}s)"
            )

            return state_type, context

        except json.JSONDecodeError:
            logger.exception("状态文件 JSON 损坏")

        except KeyError as e:
            logger.exception(
                f"未知状态类型: {e}"
            )

        except Exception:
            logger.exception("状态恢复失败")

        return None, None

    def clear(self):
        """清除状态存档"""

        try:
            if os.path.exists(self.save_file):
                os.remove(self.save_file)

                logger.info("状态存档已清除")

        except Exception:
            logger.exception("清除状态存档失败")