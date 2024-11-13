# esp32_manager/esp32_manager.py

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

    def connect(self):
        """Устанавливает соединение с ESP32."""
        self.connection.connect()

    def upload_file(self, editor):
        """Загружает файл на ESP32."""
        if editor.file_path:
            self.file_transfer.upload_file(editor.file_path)
        else:
            self.logger.log("Ошибка: Нет файла для загрузки")

    def run(self, file_path="main.py"):
        """Загружает и запускает скрипт на ESP32."""
        self.file_transfer.upload_file(file_path)
        self.reset.reset()

    def stop(self):
        """Останавливает выполнение кода на ESP32."""
        self.reset.stop()

    def erase_flash(self):
        """Стирает флеш-память ESP32."""
        self.flash_manager.erase_flash()

    def flash_firmware(self):
        """Прошивает ESP32 с использованием выбранного файла прошивки."""
        self.flash_manager.flash_firmware()