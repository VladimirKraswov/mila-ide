# esp32_manager.py
import os
import time
from PyQt6.QtWidgets import QMessageBox, QInputDialog
import subprocess
from serial.tools import list_ports

class ESP32Manager:
    def __init__(self, parent, console_widget=None):
        self.parent = parent
        self.console_widget = console_widget  # Виджет консоли для логов
        self.port = None  # Порт будет выбран пользователем
        self.baudrate = 115200
        self.connected = False

    def log(self, message):
        """Логирование сообщения в консольный виджет, если он доступен."""
        if self.console_widget:
            self.console_widget.append_log(message)
        print(message)  # Также выводим сообщение в стандартный вывод

    def select_port(self):
        """Запрашивает у пользователя выбор порта из доступных."""
        ports = [port.device for port in list_ports.comports()]
        if not ports:
            QMessageBox.warning(self.parent, "Ошибка", "Не найдено доступных портов для ESP32.")
            return None
        port, ok = QInputDialog.getItem(self.parent, "Выбор порта", "Выберите порт для ESP32:", ports, 0, False)
        if ok and port:
            self.port = port
            return port
        return None

    def connect(self):
        """Подключение к ESP32 с выбором порта."""
        if not self.select_port():
            return
        try:
            self.log(f"Попытка подключения к ESP32 на порту {self.port}...")
            result = subprocess.run(
                ["ampy", "--port", self.port, "ls"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            if result.returncode == 0:
                self.connected = True
                self.log("Успешное подключение к ESP32.")
                QMessageBox.information(self.parent, "Подключение", "Успешно подключено к ESP32.")
            else:
                raise Exception(result.stderr.decode())
        except Exception as e:
            self.log(f"Ошибка подключения: {e}")
            QMessageBox.critical(self.parent, "Ошибка подключения", f"Не удалось подключиться к ESP32: {e}")
            self.connected = False

    def upload_file(self, editor):
        """Загрузка текущего открытого файла на ESP32."""
        if not self.connected:
            QMessageBox.warning(self.parent, "Ошибка", "Сначала подключитесь к ESP32.")
            return

        file_path = editor.file_path
        if not file_path:
            QMessageBox.warning(self.parent, "Ошибка", "Файл не сохранен. Сохраните файл перед загрузкой на ESP32.")
            return

        target_path = os.path.basename(file_path)
        self.log(f"Загрузка файла {file_path} как {target_path} на ESP32...")
        try:
            result = subprocess.run(
                ["ampy", "--port", self.port, "put", file_path, target_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            if result.returncode != 0:
                raise Exception(result.stderr.decode())
            self.log(f"Файл {file_path} успешно загружен на ESP32.")
            QMessageBox.information(self.parent, "Загрузка", f"Файл {target_path} успешно загружен на ESP32.")
        except Exception as e:
            self.log(f"Ошибка загрузки: {e}")
            QMessageBox.critical(self.parent, "Ошибка загрузки", f"Не удалось загрузить файл: {e}")

    def run(self, file_path="main.py"):
      """Загружает и запускает main.py на ESP32 через программную перезагрузку."""
      if not self.connected:
          QMessageBox.warning(self.parent, "Ошибка", "Сначала подключитесь к ESP32.")
          return

      try:
          # Загрузка файла main.py на устройство
          self.log(f"Загрузка файла {file_path} как main.py на ESP32...")
          result = subprocess.run(
              ["ampy", "--port", self.port, "put", file_path, "main.py"],
              stdout=subprocess.PIPE,
              stderr=subprocess.PIPE
          )
          if result.returncode != 0:
              raise Exception(result.stderr.decode())
          self.log(f"Файл {file_path} успешно загружен на ESP32.")

          # Загрузка скрипта для перезагрузки
          self.log("Загрузка файла reset.py для перезагрузки на ESP32...")
          reset_script = "import machine\nmachine.reset()"
          with open("reset.py", "w") as f:
              f.write(reset_script)
          result_reset = subprocess.run(
              ["ampy", "--port", self.port, "put", "reset.py"],
              stdout=subprocess.PIPE,
              stderr=subprocess.PIPE
          )
          if result_reset.returncode != 0:
              raise Exception(result_reset.stderr.decode())

          # Запуск скрипта reset.py для принудительной перезагрузки
          self.log("Запуск скрипта reset.py для перезагрузки ESP32...")
          exec_reset = subprocess.run(
              ["ampy", "--port", self.port, "run", "reset.py"],
              stdout=subprocess.PIPE,
              stderr=subprocess.PIPE,
              timeout=5  # Установка тайм-аута на выполнение команды
          )
          if exec_reset.returncode != 0:
              raise Exception(exec_reset.stderr.decode())

          self.log("ESP32 успешно перезагружен и main.py запущен.")
          QMessageBox.information(self.parent, "Запуск", "Код успешно загружен и запущен на ESP32.")

          # Ожидание завершения перезагрузки перед закрытием
          time.sleep(2)
      
      except subprocess.TimeoutExpired:
          # Игнорируем тайм-аут, так как это ожидаемое поведение после reset
          self.log("ESP32 перезагружается...")

      except Exception as e:
          self.log(f"Ошибка запуска: {e}")
          QMessageBox.critical(self.parent, "Ошибка запуска", f"Не удалось запустить код: {e}")
      
      finally:
          # Удаляем временный файл reset.py
          if os.path.exists("reset.py"):
              os.remove("reset.py")

    def stop(self):
        """Останавливает выполнение кода на ESP32 через сброс устройства."""
        if not self.connected:
            QMessageBox.warning(self.parent, "Ошибка", "Сначала подключитесь к ESP32.")
            return

        try:
            self.log("Попытка остановить выполнение кода на ESP32...")
            result = subprocess.run(
                ["ampy", "--port", self.port, "run", "reset.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            if result.returncode != 0:
                raise Exception(result.stderr.decode())
            self.log("ESP32 успешно остановлен и перезагружен.")
            QMessageBox.information(self.parent, "Остановка", "ESP32 успешно перезагружен.")
        except Exception as e:
            self.log(f"Ошибка остановки: {e}")
            QMessageBox.critical(self.parent, "Ошибка остановки", f"Не удалось остановить код: {e}")