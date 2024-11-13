from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QPushButton, QHBoxLayout

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editor Settings")
        
        layout = QVBoxLayout()

        # Font size setting
        self.font_size_label = QLabel("Font Size:")
        self.font_size_spinbox = QSpinBox()
        self.font_size_spinbox.setRange(8, 48)  # Set font size range
        self.font_size_spinbox.setValue(parent.settings_manager.get_font_size())  # Set current font size from settings
        
        # Apply and Cancel buttons
        button_layout = QHBoxLayout()
        self.apply_button = QPushButton("Apply")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.cancel_button)
        
        # Add widgets to layout
        layout.addWidget(self.font_size_label)
        layout.addWidget(self.font_size_spinbox)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Connect signals
        self.apply_button.clicked.connect(self.apply_settings)
        self.cancel_button.clicked.connect(self.reject)

    def apply_settings(self):
        """Apply settings and close the dialog."""
        self.accept()

    def get_font_size(self):
        return self.font_size_spinbox.value()