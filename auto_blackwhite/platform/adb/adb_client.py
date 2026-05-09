# ADB Client for handling ADB operations in the application

import subprocess
import logging
logger = logging.getLogger("GameBot")

class ADBClient:
    def __init__(self, device_serial=None):
        self.device_serial = device_serial
    
    def _adb_cmd(self, args):
        cmd = ["adb"]
        if self.device_serial:
            cmd.extend(["-s", self.device_serial])
        cmd.extend(args)
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout.strip(), result.stderr.strip()
    
    def connect(self, addr):
        out, err = self._adb_cmd(["connect", addr])
        if "connected" in out:
            self.device_serial = addr
            return True
        logger.error(f"ADB 连接失败: {err}")
        return False
    
    def devices(self):
        out, _ = self._adb_cmd(["devices"])
        return out
    
    def shell(self, command):
        out, err = self._adb_cmd(["shell", command])
        return out
    
    def click(self, x, y):
        self.shell(f"input tap {x} {y}")
    
    def swipe(self, x1, y1, x2, y2, duration=100):
        self.shell(f"input swipe {x1} {y1} {x2} {y2} {duration}")
    
    def screenshot(self, output_path):
        self.shell(f"screencap -p /sdcard/screenshot.png")
        self._adb_cmd(["pull", "/sdcard/screenshot.png", output_path])