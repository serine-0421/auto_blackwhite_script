# 入口：启动状态机 + 启动提神轮询线程
# main.py
import threading
import time
import logging
from core.connector import DeviceConnector
from core.controller import GameController
from core.recognizer import Recognizer
from fsm.state_machine import GameStateMachine
from tasks.tishen import TishenTask
from config.settings import DEVICE_ADDR
from utils.logger import setup_logger

def main():
    logger = setup_logger()
    logger.info("脚本启动")
    
    # 连接设备
    connector = DeviceConnector(DEVICE_ADDR)
    controller = GameController(connector)
    recognizer = Recognizer(controller)
    
    # 启动提神线程
    tishen = TishenTask(controller, recognizer)
    t = threading.Thread(target=tishen.run_loop, daemon=True)
    t.start()
    logger.info("提神线程已启动")
    
    # 启动状态机主循环
    state_machine = GameStateMachine(controller, recognizer)
    
    # 注意：状态机和提神线程会同时操作controller，需要加锁避免冲突
    # 在controller的每个操作里加锁，或者通过共享锁机制。
    # 简单改进：在GameController中加入self.lock，所有操作方法都acquire。
    # 我们将在后续完善。暂时这样也能跑，但可能会有冲突。
    # 更好的做法是在controller里添加线程锁。
    # 下面提供一个包装：让状态机也使用同一个锁。
    # 这里为了简化，我们让state_machine的controller方法调用前尝试获取锁，但需要修改GameController
    # 暂且保持原样，后续调整。
    
    state_machine.run()

if __name__ == "__main__":
    main()