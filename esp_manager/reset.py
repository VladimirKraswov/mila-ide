import subprocess
import time
import os
from PySide6.QtWidgets import QMessageBox

class ESP32Reset:
    def __init__(self, logger, port):
        self.logger = logger
        self.port = port

    def reset(self):
        reset_script = "import machine\nmachine.reset()"
        with open("reset.py", "w") as f:
            f.write(reset_script)
        
        try:
            self.logger.log("Запуск скрипта reset.py для перезагрузки ESP32...")
            subprocess.run(["ampy", "--port", self.port, "put", "reset.py"], check=True)
            # Запуск reset.py с ожиданием возможного тайм-аута
            subprocess.run(["ampy", "--port", self.port, "run", "reset.py"], timeout=5, check=True)
            self.logger.log("ESP32 успешно перезагружен.")
            time.sleep(2)
        except subprocess.TimeoutExpired:
            self.logger.log("Перезагрузка ESP32 завершена (тайм-аут).")
        except Exception as e:
            self.logger.log(f"Ошибка перезагрузки: {e}")
            QMessageBox.critical(None, "Ошибка перезагрузки", f"Не удалось перезагрузить ESP32: {e}")
        finally:
            os.remove("reset.py")