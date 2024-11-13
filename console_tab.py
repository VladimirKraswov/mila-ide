# console_tab.py
import platform 
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PySide6.QtCore import QProcess, Qt, QEvent
from PySide6.QtGui import QColor, QTextCursor, QFont

class ConsoleTab(QWidget):
    def __init__(self, working_directory, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Console Tab")
        self.working_directory = working_directory

        # Layout
        layout = QVBoxLayout(self)

        # Console area (output + input in one)
        self.console_area = QTextEdit()
        self.console_area.setReadOnly(False)  # Allow typing directly in console
        self.console_area.setStyleSheet(
            """
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: "Courier New", monospace;
                font-size: 12pt;
                padding: 5px;
            }
            """
        )
        self.console_area.setFont(QFont("Courier New", 12))
        layout.addWidget(self.console_area)
        
        # Start process for executing commands
        self.process = QProcess()
        self.process.setWorkingDirectory(self.working_directory)
        self.process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.on_ready_read_output)
        self.process.readyReadStandardError.connect(self.on_ready_read_error)
        
        # Start shell
        self.start_shell()
        
        # Connect signals for handling user input
        self.console_area.installEventFilter(self)
        self.console_area.append("<span style='color: #00ff00;'>$ </span>")  # Start with a prompt

    def start_shell(self):
        """Start the interactive shell based on the OS."""
        shell_command = "/bin/bash" if platform.system() != "Windows" else "cmd.exe"
        self.process.start(shell_command)

    def eventFilter(self, source, event):
        """Filter key press events to handle enter and backspace."""
        if source == self.console_area:
            if event.type() == QEvent.Type.KeyPress:
                if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
                    self.handle_command()
                    return True
                elif event.key() == Qt.Key.Key_Backspace:
                    # Prevent deleting past the prompt
                    if self.console_area.textCursor().positionInBlock() <= 2:  # `$ ` length
                        return True
        return super().eventFilter(source, event)

    def handle_command(self):
        """Handle the command entered by the user."""
        # Get the last line (user input)
        cursor = self.console_area.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.StartOfLine, QTextCursor.MoveMode.KeepAnchor)
        user_input = cursor.selectedText().replace('$ ', '').strip()
        
        # Display the command in the console output
        self.append_output(f"<span style='color: #00ff00;'>$ {user_input}</span>")

        # Send the command to the process
        self.process.write((user_input + '\n').encode())

        # Prepare for the next command
        self.console_area.append("<span style='color: #00ff00;'>$ </span>")
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.console_area.setTextCursor(cursor)

    def on_ready_read_output(self):
        """Append command output to the console."""
        output = self.process.readAllStandardOutput().data().decode()
        styled_output = f"<span style='color: #d4d4d4;'>{output}</span>"
        self.append_output(styled_output)

    def on_ready_read_error(self):
        """Append command error output to the console."""
        error_output = self.process.readAllStandardError().data().decode()
        styled_error = f"<span style='color: #ff0000;'>{error_output}</span>"
        self.append_output(styled_error)

    def append_output(self, text):
        """Append styled text to the console area."""
        self.console_area.moveCursor(QTextCursor.MoveOperation.End)
        self.console_area.insertHtml(text + "<br>")
        self.console_area.moveCursor(QTextCursor.MoveOperation.End)