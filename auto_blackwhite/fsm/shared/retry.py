# 重试机制

import time
import logging
logger = logging.getLogger("GameBot")

def retry_on_failure(func, max_retries=3, delay=2, exceptions=(Exception,)):
    """重试装饰器"""
    for attempt in range(max_retries):
        try:
            return func()
        except exceptions as e:
            logger.warning(f"重试 {attempt+1}/{max_retries}: {e}")
            time.sleep(delay)
    raise Exception(f"重试 {max_retries} 次后失败")