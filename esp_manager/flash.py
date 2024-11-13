import esptool
import os
from PyQt6.QtWidgets import QMessageBox

class FlashManager:
    def __init__(self, logger, port, baudrate=115200):
        self.logger = logger
        self.port = port
        self.baudrate = baudrate

    def erase_flash(self):
        self.logger.log("Стирание флеш-памяти ESP32...")
        try:
            esptool.main(["--port", self.port, "--baud", str(self.baudrate), "erase_flash"])
            self.logger.log("Флеш-память ESP32 успешно стёрта.")
        except Exception as e:
            self.logger.log(f"Ошибка стирания флеш-памяти: {e}")
            QMessageBox.critical(None, "Ошибка стирания флеш-памяти", f"Не удалось стереть флеш-память: {e}")

    def flash_firmware(self, firmware_path):
        chip_type = "esp32" if "ESP32" in firmware_path.upper() else "esp8266"
        self.logger.log(f"Прошивка микроконтроллера с использованием {firmware_path}...")
        try:
            esptool.main([
                "--chip", chip_type, "--port", self.port,
                "--baud", str(self.baudrate), "write_flash", "-z", "0x1000", firmware_path
            ])
            self.logger.log(f"Прошивка {firmware_path} успешно завершена.")
        except Exception as e:
            self.logger.log(f"Ошибка прошивки: {e}")
            QMessageBox.critical(None, "Ошибка прошивки", f"Не удалось прошить микроконтроллер: {e}")