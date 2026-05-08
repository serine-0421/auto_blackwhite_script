# 监控模拟器/ADB连接是否存活

import time
import subprocess
import logging
from tasks.base_task import BaseTask

logger = logging.getLogger("GameBot")

class WatchdogTask(BaseTask):
    """监控模拟器和ADB连接状态，必要时重启"""
    
    def __init__(self, controller, recognizer, interval_seconds=60, 
                 adb_device_serial="127.0.0.1:5555", 
                 simulator_process_name="ldplayer9.exe"):
        super().__init__(controller, recognizer, interval_seconds)
        self.adb_serial = adb_device_serial
        self.simulator_process_name = simulator_process_name
        self.consecutive_failures = 0
        self.max_failures = 3   # 连续失败次数阈值，触发重启模拟器
    
    def execute_once(self):
        """检查设备连接和模拟器进程"""
        # 1. 检查ADB连接
        if not self._check_adb_connection():
            logger.warning("ADB 连接异常")
            self.consecutive_failures += 1
            if self.consecutive_failures >= self.max_failures:
                logger.error("连续多次ADB失败，尝试重启模拟器")
                self._restart_simulator()
                self.consecutive_failures = 0
            return
        
        # 2. 检查模拟器进程是否存活（可选）
        if not self._check_simulator_running():
            logger.warning("模拟器进程未运行，尝试启动")
            self._start_simulator()
            time.sleep(10)  # 等待启动
            # 尝试重连ADB
            self._reconnect_adb()
            self.consecutive_failures = 0
        else:
            self.consecutive_failures = 0
    
    def _check_adb_connection(self) -> bool:
        """通过 adb devices 检查设备是否在线"""
        try:
            result = subprocess.run(
                ["adb", "devices"],
                capture_output=True, text=True, timeout=10
            )
            output = result.stdout
            if self.adb_serial in output and "device" in output:
                return True
            else:
                logger.debug(f"ADB 未找到设备 {self.adb_serial}")
                return False
        except Exception as e:
            logger.error(f"ADB 检查失败: {e}")
            return False
    
    def _check_simulator_running(self) -> bool:
        """Windows下检查进程是否存在（Linux下需适配）"""
        import platform
        if platform.system() == "Windows":
            try:
                result = subprocess.run(
                    ["tasklist", "/FI", f"IMAGENAME eq {self.simulator_process_name}"],
                    capture_output=True, text=True
                )
                return self.simulator_process_name in result.stdout
            except:
                return True   # 无法判断时认为运行中
        else:
            # Linux 下可以通过 pgrep 检查
            try:
                result = subprocess.run(["pgrep", "-f", self.simulator_process_name], capture_output=True)
                return result.returncode == 0
            except:
                return True
    
    def _restart_simulator(self):
        """重启模拟器（先关闭再启动）"""
        logger.warning("正在重启模拟器...")
        self._stop_simulator()
        time.sleep(3)
        self._start_simulator()
        time.sleep(10)
        self._reconnect_adb()
    
    def _stop_simulator(self):
        """关闭模拟器进程"""
        import platform
        if platform.system() == "Windows":
            subprocess.run(["taskkill", "/f", "/im", self.simulator_process_name], capture_output=True)
        else:
            subprocess.run(["pkill", "-f", self.simulator_process_name], capture_output=True)
        logger.info("模拟器已关闭")
    
    def _start_simulator(self):
        """启动模拟器（需要知道启动命令，通常为模拟器安装路径下的可执行文件）"""
        # 请根据实际安装路径修改
        # 例如雷电模拟器：start D:/LDPlayer/ldplayer9.exe
        start_cmd = ["start", "D:/LDPlayer/ldplayer9.exe"]  # Windows
        import platform
        if platform.system() == "Windows":
            subprocess.Popen(start_cmd, shell=True)
        else:
            # Linux 下可能需要 waydroid 启动命令
            subprocess.Popen(["waydroid", "session", "start"])
        logger.info("模拟器启动命令已执行")
    
    def _reconnect_adb(self):
        """重新连接ADB"""
        subprocess.run(["adb", "kill-server"], capture_output=True)
        time.sleep(1)
        subprocess.run(["adb", "start-server"], capture_output=True)
        time.sleep(2)
        subprocess.run(["adb", "connect", self.adb_serial], capture_output=True)
        logger.info("ADB 重连完成")