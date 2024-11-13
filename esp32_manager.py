from esp_manager.logger import Logger
from esp_manager.connection import ESP32Connection
from esp_manager.file_transfer import FileTransfer
from esp_manager.reset import ESP32Reset
from esp_manager.flash import FlashManager
from esp_manager.utils import select_port

class ESP32Manager:
    def __init__(self, parent, console_widget=None):
        self.logger = Logger(console_widget)
        self.port = select_port(parent)
        self.connection = ESP32Connection(self.logger, parent, self.port)
        self.file_transfer = FileTransfer(self.logger, self.port)
        self.reset = ESP32Reset(self.logger, self.port)
        self.flash_manager = FlashManager(self.logger, self.port)
        self.parent = parent