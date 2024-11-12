# main_menu.py
from PyQt6.QtWidgets import QMenuBar, QMenu, QFileDialog
from PyQt6.QtGui import QAction  # Изменили импорт на PyQt6.QtGui
from PyQt6.QtCore import Qt

class MainMenu(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Меню "Файл"
        file_menu = self.addMenu("Файл")

        open_file_action = QAction("Открыть файл", self)
        open_file_action.triggered.connect(parent.open_file)
        file_menu.addAction(open_file_action)

        open_directory_action = QAction("Выбрать директорию", self)
        open_directory_action.triggered.connect(parent.open_directory)
        file_menu.addAction(open_directory_action)

        save_action = QAction("Сохранить", self)
        save_action.triggered.connect(parent.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction("Сохранить как", self)
        save_as_action.triggered.connect(parent.save_file_as)
        file_menu.addAction(save_as_action)

        save_all_action = QAction("Сохранить все", self)
        save_all_action.triggered.connect(parent.save_all_files)
        file_menu.addAction(save_all_action)

        # Меню "Редактировать"
        edit_menu = self.addMenu("Редактировать")

        copy_action = QAction("Копировать", self)
        # copy_action.triggered.connect(parent.editor_tabs.copy)
        edit_menu.addAction(copy_action)

        paste_action = QAction("Вставить", self)
        # paste_action.triggered.connect(parent.editor_tabs.paste)
        edit_menu.addAction(paste_action)

        cut_action = QAction("Вырезать", self)
        # cut_action.triggered.connect(parent.editor_tabs.cut)
        edit_menu.addAction(cut_action)

        undo_action = QAction("Отменить", self)
        # undo_action.triggered.connect(parent.editor_tabs.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction("Вернуть", self)
        # redo_action.triggered.connect(parent.editor_tabs.redo)
        edit_menu.addAction(redo_action)

        # Settings menu
        settings_menu = self.addMenu("Settings")
        editor_settings_action = QAction("Editor", self)
        # editor_settings_action.triggered.connect(parent.open_editor_settings)
        settings_menu.addAction(editor_settings_action)

        # Меню "О программа"
        about_menu = self.addMenu("О программа")

        about_action = QAction("О программе", self)
        # about_action.triggered.connect(parent.show_about)
        about_menu.addAction(about_action)