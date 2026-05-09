# LDPlayer Emulator for handling LDPlayer-specific emulator operations in the application

import subprocess
import logging
from platform.emulator.base import EmulatorBase

logger = logging.getLogger("GameBot")

class LDPlayer(EmulatorBase):
    def __init__(self, ld_console_path="D:/LDPlayer/ldconsole.exe", index=0):
        self.ld_console = ld_console_path
        self.index = index
    
    def start(self):
        subprocess.run([self.ld_console, "launch", "--index", str(self.index)])
    
    def stop(self):
        subprocess.run([self.ld_console, "quit", "--index", str(self.index)])
    
    def restart(self):
        self.stop()
        self.start()
    
    def get_adb_port(self):
        return 5555 + self.index * 2