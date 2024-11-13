import os
from PySide6.QtWidgets import QFileDialog, QMessageBox

class FileManager:
    def __init__(self, parent):
        self.parent = parent  # Reference to MainWindow for dialogs

    def open_file(self, editor):
        file_name, _ = QFileDialog.getOpenFileName(self.parent, "Open File")
        if file_name:
            content = self.read_file(file_name)
            editor.setPlainText(content)

    def save_file(self, editor):
        content = editor.toPlainText()
        file_name, _ = QFileDialog.getSaveFileName(self.parent, "Save File")
        if file_name:
            self.write_file(file_name, content)

    def save_file_as(self, editor):
        content = editor.toPlainText()
        file_name, _ = QFileDialog.getSaveFileName(self.parent, "Save File As")
        if file_name:
            self.write_file(file_name, content)

    def save_all_files(self, editor):
        self.save_file(editor)  # Placeholder for future multi-file support

    def file_exists(self, file_path):
        """Check if a file exists at the given path."""
        return os.path.isfile(file_path)

    def read_file(self, file_path):
        """Read the content of a file and return it."""
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except Exception as e:
            QMessageBox.warning(self.parent, "Error", f"Could not read file: {e}")
            return ""

    def write_file(self, file_path, content):
        """Write content to a file at the specified path."""
        try:
            with open(file_path, 'w') as file:
                file.write(content)
        except Exception as e:
            QMessageBox.warning(self.parent, "Error", f"Could not save file: {e}")

    def get_file_name(self, file_path):
        """Extract and return the file name from the path."""
        return os.path.basename(file_path)
    
    def get_file_path(self, editor):
        """Получает путь к файлу, если он был сохранен, иначе возвращает None."""
        # Проверим, если у редактора есть привязанный путь
        if hasattr(editor, "file_path"):
            return editor.file_path
        return None