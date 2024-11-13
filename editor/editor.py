# editor/editor.py
from PySide6.QtWidgets import QTextEdit, QTabWidget
from PySide6.QtGui import QFont, QPainter, QColor
from PySide6.QtCore import Qt
from .line_numbers import LineNumberArea
from .highlighter import PygmentsHighlighter
from .completer import CodeCompleter

class CodeEditor(QTextEdit):
    def __init__(self, file_path=None, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Courier New", 10))
        self.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4;")
        self.file_path = file_path  # Атрибут для хранения пути к файлу
        
        # Line numbers
        self.line_number_area = LineNumberArea(self)
        self.highlighter = PygmentsHighlighter(self.document())  # Syntax highlighting

        # Autocompletion
        self.completer = CodeCompleter(self)

    def open_file(self, file_path):
        """Open a file and load its contents into the editor."""
        self.file_path = file_path
        with open(file_path, 'r') as file:
            self.setPlainText(file.read())

    def save_file(self):
        """Save the current contents to the file."""
        if self.file_path:
            with open(self.file_path, 'w') as file:
                file.write(self.toPlainText())

    def line_number_area_width(self):
        return 40

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(cr.left(), cr.top(), self.line_number_area_width(), cr.height())
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor(50, 50, 50))

        block = self.document().firstBlock()
        block_number = block.blockNumber()
        top = int(self.document().documentLayout().blockBoundingRect(block).top())
        bottom = top + int(self.document().documentLayout().blockBoundingRect(block).height())
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.GlobalColor.lightGray)
                painter.drawText(0, top, self.line_number_area.width() - 5, self.fontMetrics().height(), Qt.AlignmentFlag.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + int(self.document().documentLayout().blockBoundingRect(block).height())
            block_number += 1

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.text().isalnum() or event.text() == '.':
            text = self.toPlainText()
            line, column = self.textCursor().blockNumber() + 1, self.textCursor().columnNumber()
            self.completer.show_completions(text, line, column)
        
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            cursor = self.textCursor()
            cursor.movePosition(cursor.MoveOperation.StartOfLine)
            cursor.select(cursor.SelectionType.LineUnderCursor)
            prev_line = cursor.selectedText()
            indent = len(prev_line) - len(prev_line.lstrip())
            cursor.insertText("\n" + " " * indent)


class TabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)

    def add_code_editor(self, file_name, file_path=None, content=""):
        """Add a new tab with a CodeEditor, setting the file path if provided."""
        editor = CodeEditor(file_path)
        editor.setPlainText(content)
        editor.file_path = file_path  # Устанавливаем путь к файлу в редакторе
        index = self.addTab(editor, file_name)
        self.setCurrentIndex(index)

    def get_current_editor(self):
        """Return the currently active CodeEditor."""
        return self.currentWidget()

    def close_tab(self, index):
        """Close the tab at the specified index."""
        self.removeTab(index)