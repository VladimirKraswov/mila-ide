import subprocess
from PyQt6.QtWidgets import QMessageBox

class ESP32Connection:
    def __init__(self, logger, parent, port, baudrate=115200):
        self.logger = logger
        self.parent = parent
        self.port = port
        self.baudrate = baudrate
        self.connected = False

    def connect(self):
        if not self.port:
            return
        try:
            self.logger.log(f"Попытка подключения к ESP32 на порту {self.port}...")
            result = subprocess.run(["ampy", "--port", self.port, "ls"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                self.connected = True
                self.logger.log("Успешное подключение к ESP32.")
                QMessageBox.information(self.parent, "Подключение", "Успешно подключено к ESP32.")
            else:
                raise Exception(result.stderr.decode())
        except Exception as e:
            self.logger.log(f"Ошибка подключения: {e}")
            QMessageBox.critical(self.parent, "Ошибка подключения", f"Не удалось подключиться к ESP32: {e}")
            self.connected = False