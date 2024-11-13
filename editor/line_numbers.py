# editor/line_numbers.py
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def paintEvent(self, event):
        self.code_editor.line_number_area_paint_event(event)
