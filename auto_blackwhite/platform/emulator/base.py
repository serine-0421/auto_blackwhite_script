# Base Emulator for handling emulator operations in the application

from abc import ABC, abstractmethod

class EmulatorBase(ABC):
    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def stop(self):
        pass
    
    @abstractmethod
    def restart(self):
        pass
    
    @abstractmethod
    def get_adb_port(self):
        pass