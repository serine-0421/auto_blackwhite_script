# ADB Check for validating ADB connectivity in the application

class ADBCheck:
    def __init__(self, controller):
        self.controller = controller
    
    def passed(self):
        try:
            # 尝试获取设备信息
            self.controller.connector.ensure_connected()
            return True
        except:
            return False
    
    def get_recovery_action(self):
        return "reconnect_adb"