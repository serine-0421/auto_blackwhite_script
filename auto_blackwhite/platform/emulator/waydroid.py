# Waydroid Emulator for handling Waydroid-specific emulator operations in the application

import subprocess
import logging
from platform.emulator.base import EmulatorBase

logger = logging.getLogger("GameBot")

class Waydroid(EmulatorBase):
    def start(self):
        subprocess.run(["waydroid", "session", "start"])
    
    def stop(self):
        subprocess.run(["waydroid", "session", "stop"])
    
    def restart(self):
        self.stop()
        self.start()
    
    def get_adb_port(self):
        return 5555  