from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from console_tab import ConsoleTab

class ConsoleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Console")
        
        # Layout
        layout = QVBoxLayout(self)
        
        # Tab widget for multiple consoles
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        
        # Add tab widget to layout
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
        
        # Default console tab for logs
        self.add_console_tab(".")  # Рабочий каталог по умолчанию

    def add_console_tab(self, working_directory):
        """Add a new console tab with the specified working directory."""
        console_tab = ConsoleTab(working_directory)
        index = self.tab_widget.addTab(console_tab, f"Console {self.tab_widget.count() + 1}")
        self.tab_widget.setCurrentIndex(index)

    def close_tab(self, index):
        """Close the specified tab."""
        self.tab_widget.removeTab(index)
        
    def append_log(self, message):
        """Append a log message to the current console output area."""
        current_console = self.tab_widget.currentWidget()
        if current_console:
            current_console.append_output(f"[LOG] {message}")