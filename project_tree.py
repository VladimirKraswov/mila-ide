# project_tree.py
import os
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt6.QtCore import Qt

class ProjectTree(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderHidden(True)  # Hide header
        self.setMinimumWidth(200)
        self.itemDoubleClicked.connect(self.open_file)

    def load_directory(self, path):
        """Load the directory into the project tree."""
        self.clear()
        root = QTreeWidgetItem(self, [os.path.basename(path) or path])
        root.setData(0, Qt.ItemDataRole.UserRole, path)
        self.add_tree_items(root, path)
        root.setExpanded(True)

    def add_tree_items(self, parent_item, path):
        """Recursively add directories and files to the tree, with error handling for permissions."""
        try:
            for file_name in os.listdir(path):
                full_path = os.path.join(path, file_name)
                child_item = QTreeWidgetItem(parent_item, [file_name])
                child_item.setData(0, Qt.ItemDataRole.UserRole, full_path)
                if os.path.isdir(full_path):
                    self.add_tree_items(child_item, full_path)
        except PermissionError:
            # Skip directories where access is denied
            print(f"Permission denied: {path}")

    def open_file(self, item):
        """Emit a signal to open a file when double-clicked in the project tree."""
        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        if os.path.isfile(file_path):
            # Emit a custom signal here to open the file in the editor, if needed
            print(f"Open file: {file_path}")