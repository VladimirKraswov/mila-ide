import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSplitter, QMessageBox, QToolBar
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from editor.editor import TabWidget, CodeEditor 
from main_menu import MainMenu
from project_tree import ProjectTree
from settings_manager import SettingsManager
from file_manager import FileManager
from actions.editor_actions import EditorActions
from actions.project_actions import ProjectActions
from console_widget import ConsoleWidget
from esp_manager.esp32_manager import ESP32Manager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mila-IDE")
        self.resize(1000, 600)

        # Initialize components
        self.settings_manager = SettingsManager()
        self.file_manager = FileManager(self)
        self.editor_tabs = TabWidget() 
        self.project_tree = ProjectTree()
        self.console_widget = ConsoleWidget()  # Initialize ConsoleWidget
        self.esp32_manager = ESP32Manager(self, self.console_widget)  # Инициализация ESP32Manager

        # Initialize actions
        self.editor_actions = EditorActions(self.editor_tabs, self.settings_manager)
        self.project_actions = ProjectActions(self.project_tree, self.file_manager)

        # Apply initial settings
        self.editor_actions.apply_editor_settings()

        # Set up main layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Splitter for project tree, editor tabs, and console
        editor_splitter = QSplitter(Qt.Orientation.Horizontal)
        editor_splitter.addWidget(self.project_tree)
        editor_splitter.addWidget(self.editor_tabs)
        editor_splitter.setStretchFactor(1, 3)

        splitter.addWidget(editor_splitter)
        splitter.addWidget(self.console_widget)  # Console widget below editor tabs
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)

        main_layout.addWidget(splitter)
        self.setCentralWidget(main_widget)

        # Main menu
        self.menu_bar = MainMenu(self)
        self.setMenuBar(self.menu_bar)

        # Toolbar
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)

        # Toolbar actions
        connect_action = QAction("Коннект", self)
        connect_action.triggered.connect(self.connect_device)
        self.toolbar.addAction(connect_action)

        upload_action = QAction("Загрузить файлы", self)  # Кнопка загрузки файлов
        upload_action.triggered.connect(self.upload_files)
        self.toolbar.addAction(upload_action)

        run_action = QAction("Запустить", self)
        run_action.triggered.connect(self.run_code)
        self.toolbar.addAction(run_action)

        stop_action = QAction("Остановить", self)
        stop_action.triggered.connect(self.stop_code)
        self.toolbar.addAction(stop_action)

        # Connect signals
        self.project_tree.itemDoubleClicked.connect(lambda item: self.open_file_from_tree(item))

    def open_file_from_tree(self, item):
        """Opens a file from the project tree in a new tab."""
        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        if file_path and self.file_manager.file_exists(file_path):
            content = self.file_manager.read_file(file_path)
            file_name = self.file_manager.get_file_name(file_path)
            self.editor_tabs.add_code_editor(file_name, file_path, content)  # Передаем file_path

    def open_directory(self):
        """Open a directory and load it into the project tree."""
        self.project_actions.open_directory()
        project_dir = self.project_actions.get_current_project_directory()
        
        # Automatically add a console tab with the selected project directory as the working directory
        if project_dir:
            self.console_widget.add_console_tab(project_dir)

    def open_file(self):
        self.file_manager.open_file(self.editor_tabs)

    def save_file(self):
        current_editor = self.editor_tabs.get_current_editor()
        if current_editor:
            self.file_manager.save_file(current_editor)

    def save_file_as(self):
        current_editor = self.editor_tabs.get_current_editor()
        if current_editor:
            self.file_manager.save_file_as(current_editor)

    def save_all_files(self):
        for i in range(self.editor_tabs.count()):
            editor = self.editor_tabs.widget(i)
            if editor:
                self.file_manager.save_file(editor)

    def open_editor_settings(self):
        self.editor_actions.open_editor_settings(self)

    def show_about(self):
        QMessageBox.about(self, "About Mila-IDE", "Mila-IDE\nA simple IDE built with PyQt6.")
    
    def open_console_tab(self):
        """Open a new console tab in ConsoleWidget with the project directory as working directory."""
        project_dir = self.project_actions.get_current_project_directory()
        self.console_widget.add_console_tab(project_dir if project_dir else ".")

    # Toolbar action methods
    def connect_device(self):
        """Подключение к ESP32."""
        self.esp32_manager.connect()

    def upload_files(self):
        """Загрузка файла из текущей вкладки на ESP32."""
        current_editor = self.editor_tabs.get_current_editor()
        if current_editor and isinstance(current_editor, CodeEditor):
            self.esp32_manager.upload_file(current_editor)
        else:
            QMessageBox.warning(self, "Ошибка", "Нет активного файла для загрузки.")

    def run_code(self):
        """Загрузка и запуск текущего файла на ESP32 через перезагрузку."""
        current_editor = self.editor_tabs.get_current_editor()
        if current_editor and current_editor.file_path:
            self.esp32_manager.run(current_editor.file_path)
        else:
            QMessageBox.warning(self, "Ошибка", "Нет активного файла для запуска.")

    def stop_code(self):
        """Остановка кода на ESP32."""
        self.esp32_manager.stop()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())