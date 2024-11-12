# actions/project_actions.py
from PyQt6.QtCore import Qt  # Add this line
from PyQt6.QtWidgets import QFileDialog
import os

class ProjectActions:
    def __init__(self, project_tree, file_manager):
        self.project_tree = project_tree
        self.file_manager = file_manager
        self.current_project_directory = None 

    def open_directory(self):
        directory = QFileDialog.getExistingDirectory(self.project_tree, "Open Directory")
        if directory:
            self.project_tree.load_directory(directory)

    def open_file_from_tree(self, item, editor_tabs):
        """Open a file from the project tree in a new editor tab."""
        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        if file_path and self.file_manager.file_exists(file_path):
            content = self.file_manager.read_file(file_path)
            file_name = self.file_manager.get_file_name(file_path)
            editor_tabs.add_code_editor(file_name, content)  # Add a new tab with file content
    
    def get_current_project_directory(self):
        """Return the path of the currently opened project directory."""
        return self.current_project_directory