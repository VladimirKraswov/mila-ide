# editor/highlighter.py
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name

class PygmentsHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.lexer = PythonLexer()
        self.style = get_style_by_name("monokai")
        self.formats = self.create_formats()

    def create_formats(self):
        formats = {}
        for token, style_def in self.style:
            qformat = QTextCharFormat()
            if style_def['color']:
                qformat.setForeground(QColor(f"#{style_def['color']}"))
            if style_def['bold']:
                qformat.setFontWeight(QFont.Weight.Bold)
            if style_def['italic']:
                qformat.setFontItalic(True)
            if style_def['bgcolor']:
                qformat.setBackground(QColor(f"#{style_def['bgcolor']}"))
            formats[token] = qformat
        return formats

    def highlightBlock(self, text):
        tokens = self.lexer.get_tokens(text)
        offset = 0
        for ttype, value in tokens:
            length = len(value)
            format = self.formats.get(ttype, QTextCharFormat())
            self.setFormat(offset, length, format)
            offset += length
