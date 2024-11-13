from PySide6.QtWidgets import QMessageBox, QInputDialog
from serial.tools import list_ports

def select_port(parent):
    ports = [port.device for port in list_ports.comports()]
    if not ports:
        QMessageBox.warning(parent, "Ошибка", "Не найдено доступных портов для ESP32.")
        return None
    port, ok = QInputDialog.getItem(parent, "Выбор порта", "Выберите порт для ESP32:", ports, 0, False)
    return port if ok else None