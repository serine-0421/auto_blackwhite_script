# 计时器

import time

class CooldownTimer:
    """冷却计时器"""
    def __init__(self, duration):
        self.duration = duration
        self.last_time = 0
    
    def is_ready(self):
        return time.time() - self.last_time >= self.duration
    
    def reset(self):
        self.last_time = time.time()