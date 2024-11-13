import subprocess
import os
from PySide6.QtWidgets import QMessageBox

class FileTransfer:
    def __init__(self, logger, port):
        self.logger = logger
        self.port = port

    def upload_file(self, file_path):
        target_path = os.path.basename(file_path)
        self.logger.log(f"Загрузка файла {file_path} как {target_path} на ESP32...")
        try:
            result = subprocess.run(
                ["ampy", "--port", self.port, "put", file_path, target_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            if result.returncode != 0:
                raise Exception(result.stderr.decode())
            self.logger.log(f"Файл {file_path} успешно загружен на ESP32.")
        except Exception as e:
            self.logger.log(f"Ошибка загрузки: {e}")
            QMessageBox.critical(None, "Ошибка загрузки", f"Не удалось загрузить файл: {e}")