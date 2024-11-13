import os
import shutil
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QMenu, QInputDialog, QMessageBox
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag, QBrush, QColor, QIcon
import qtawesome as qta

class ProjectTree(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Настройка иконок для разных типов файлов с указанием цвета
        self.file_icons = {
            ".txt": qta.icon('fa5s.file-alt', color='white'),       # Белая иконка для текстовых файлов
            ".py": QIcon("icons/python_icon.png"),            # Логотип Python для Python файлов
            ".json": qta.icon('fa5s.file-code', color='green'),     # Зеленая иконка для JSON
            ".gitignore": qta.icon('fa5s.cog', color='grey'),       # Серая иконка для .gitignore
            "default": qta.icon('fa5s.file', color='black')         # Черная иконка по умолчанию для файлов
        }
        
    def get_icon_for_file(self, file_name):
        """Выбор иконки на основе расширения файла."""
        extension = os.path.splitext(file_name)[1].lower()
        return self.file_icons.get(extension, self.file_icons["default"])
    
    def load_directory(self, path):
        """Load the directory into the project tree."""
        self.clear()
        root = QTreeWidgetItem(self, [os.path.basename(path) or path])
        root.setData(0, Qt.ItemDataRole.UserRole, path)
        self.add_tree_items(root, path)
        root.setExpanded(True)
    
    def add_tree_items(self, parent_item, path):
        """Добавление элементов в дерево с соответствующими иконками."""
        try:
            for file_name in os.listdir(path):
                full_path = os.path.join(path, file_name)
                child_item = QTreeWidgetItem(parent_item, [file_name])
                child_item.setData(0, Qt.ItemDataRole.UserRole, full_path)
                
                # Применяем иконку на основе типа файла или директории
                if os.path.isdir(full_path):
                    child_item.setIcon(0, qta.icon('fa5s.folder', color='gold'))  # Желтая иконка для папок
                    self.add_tree_items(child_item, full_path)
                else:
                    child_item.setIcon(0, self.get_icon_for_file(file_name))
        except PermissionError:
            print(f"Permission denied: {path}")

    def open_file(self, item):
        """Emit a signal to open a file when double-clicked in the project tree."""
        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        if os.path.isfile(file_path):
            print(f"Open file: {file_path}")

    def contextMenuEvent(self, event):
        """Show a context menu for creating, deleting, and renaming files and folders."""
        menu = QMenu(self)
        create_file_action = menu.addAction("Создать файл")
        create_folder_action = menu.addAction("Создать папку")
        delete_action = menu.addAction("Удалить")
        rename_action = menu.addAction("Переименовать")

        action = menu.exec(event.globalPos())
        
        if action == create_file_action:
            self.create_file_or_folder(is_folder=False)
        elif action == create_folder_action:
            self.create_file_or_folder(is_folder=True)
        elif action == delete_action:
            self.delete_item()
        elif action == rename_action:
            self.rename_item()

    def create_file_or_folder(self, is_folder):
        """Create a new file or folder in the selected directory."""
        item = self.currentItem()
        if not item:
            QMessageBox.warning(self, "Ошибка", "Выберите папку для создания нового элемента.")
            return

        parent_path = item.data(0, Qt.ItemDataRole.UserRole)
        
        # Проверяем, что выбранный элемент является директорией
        if not os.path.isdir(parent_path):
            QMessageBox.warning(self, "Ошибка", "Нельзя создать файл или папку внутри файла. Выберите папку.")
            return

        name, ok = QInputDialog.getText(
            self, "Создать папку" if is_folder else "Создать файл",
            "Введите имя новой папки:" if is_folder else "Введите имя нового файла:"
        )

        if ok and name:
            new_path = os.path.join(parent_path, name)
            try:
                if is_folder:
                    os.makedirs(new_path, exist_ok=True)
                    new_item = QTreeWidgetItem(item, [name])
                    new_item.setData(0, Qt.ItemDataRole.UserRole, new_path)
                    new_item.setIcon(0, qta.icon('fa5s.folder', color='gold'))  # Желтая иконка для папок
                else:
                    with open(new_path, 'w') as f:
                        pass
                    new_item = QTreeWidgetItem(item, [name])
                    new_item.setData(0, Qt.ItemDataRole.UserRole, new_path)
                    new_item.setIcon(0, self.get_icon_for_file(name))  # Иконка для файлов

                item.setExpanded(True)  # Оставляем текущую папку открытой
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось создать элемент: {e}")

    def delete_item(self):
        """Delete the selected file or folder."""
        item = self.currentItem()
        if not item:
            return

        path = item.data(0, Qt.ItemDataRole.UserRole)
        confirm = QMessageBox.question(
            self, "Подтвердите удаление", f"Вы уверены, что хотите удалить '{os.path.basename(path)}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)  # Удаление непустого каталога
                else:
                    os.remove(path)  # Удаление файла
                parent = item.parent() or self.invisibleRootItem()
                parent.removeChild(item)
                if self.logger:
                    self.logger.log(f"Удалено: {path}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка удаления", f"Не удалось удалить: {e}")

    def rename_item(self):
        """Rename the selected file or folder."""
        item = self.currentItem()
        if not item:
            return

        path = item.data(0, Qt.ItemDataRole.UserRole)
        new_name, ok = QInputDialog.getText(self, "Переименовать", "Введите новое имя:", text=os.path.basename(path))
        
        if ok and new_name:
            new_path = os.path.join(os.path.dirname(path), new_name)
            try:
                os.rename(path, new_path)
                item.setText(0, new_name)
                item.setData(0, Qt.ItemDataRole.UserRole, new_path)
                if self.logger:
                    self.logger.log(f"Переименовано: {path} -> {new_path}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка переименования", f"Не удалось переименовать: {e}")

    def startDrag(self, supportedActions):
        """Initialize drag operation."""
        item = self.currentItem()
        if not item:
            return
        
        mime_data = QMimeData()
        mime_data.setText(item.data(0, Qt.ItemDataRole.UserRole))
        
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.exec(supportedActions)

    def dragEnterEvent(self, event):
        """Handle drag enter event."""
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        """Handle drag move event with item highlighting."""
        target_item = self.itemAt(event.position().toPoint())
        if target_item and target_item != self.highlighted_item:
            # Remove highlight from the previous item
            if self.highlighted_item:
                self.highlighted_item.setBackground(0, QBrush(Qt.GlobalColor.transparent))

            # Highlight the new target item
            target_item.setBackground(0, QBrush(QColor(200, 200, 255)))  # Light blue highlight
            self.highlighted_item = target_item

        event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        """Remove highlighting when drag leaves the tree widget."""
        if self.highlighted_item:
            self.highlighted_item.setBackground(0, QBrush(Qt.GlobalColor.transparent))
            self.highlighted_item = None

    def dropEvent(self, event):
        """Handle drop event."""
        source_path = event.mimeData().text()
        target_item = self.itemAt(event.position().toPoint())
        
        if target_item:
            # Remove highlight from the target item after dropping
            if self.highlighted_item:
                self.highlighted_item.setBackground(0, QBrush(Qt.GlobalColor.transparent))
                self.highlighted_item = None

            target_path = target_item.data(0, Qt.ItemDataRole.UserRole)
            if os.path.isdir(target_path):
                # Get the file/folder name
                item_name = os.path.basename(source_path)
                new_path = os.path.join(target_path, item_name)

                try:
                    os.rename(source_path, new_path)
                    self.load_directory(os.path.dirname(target_path))  # Refresh tree at target path
                    if self.logger:
                        self.logger.log(f"Перемещено {source_path} -> {new_path}")
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка перемещения", f"Не удалось переместить: {e}")

        event.acceptProposedAction()