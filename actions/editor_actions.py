from PySide6.QtWidgets import QDialog
from PySide6.QtGui import QFont
from settings_dialog import SettingsDialog

class EditorActions:
    def __init__(self, editor_tabs, settings_manager):
        self.editor_tabs = editor_tabs
        self.settings_manager = settings_manager

    def apply_editor_settings(self):
        """Apply font settings to all open editor tabs."""
        font_size = self.settings_manager.get_font_size()
        for i in range(self.editor_tabs.count()):
            editor = self.editor_tabs.widget(i)
            if editor:
                editor.setFont(QFont("Courier New", font_size))

    def open_editor_settings(self, parent):
        """Open settings dialog to adjust editor settings."""
        dialog = SettingsDialog(parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_font_size = dialog.get_font_size()
            self.settings_manager.set_font_size(new_font_size)
            self.settings_manager.save_settings()
            self.apply_editor_settings()