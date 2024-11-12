# editor/line_numbers.py
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def paintEvent(self, event):
        self.code_editor.line_number_area_paint_event(event)
