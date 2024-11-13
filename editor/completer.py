# editor/completer.py
from PySide6.QtWidgets import QListWidget, QListWidgetItem
from PySide6.QtCore import Qt, QPoint
import jedi

class CodeCompleter(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Popup)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)  # Окно подсказок не перехватывает фокус
        self.setVisible(False)  # Подсказки скрыты по умолчанию
        self.setStyleSheet("background-color: #2e2e2e; color: white; border: 1px solid #444;")

        # Позволяем листу подсказок двигаться по стрелкам, но не блокируем основной фокус
        self.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.itemClicked.connect(self.insert_completion)

    def show_completions(self, text, line, column):
        # Запрашиваем подсказки у jedi
        script = jedi.Script(text)
        completions = script.complete(line=line, column=column)

        # if completions:
        #     self.clear()  # Очищаем старые подсказки
        #     for completion in completions:
        #         item = QListWidgetItem(completion.name)
        #         self.addItem(item)

        #     cursor_rect = self.parent().cursorRect()
        #     editor_global_pos = self.parent().mapToGlobal(cursor_rect.bottomRight())
        #     self.move(editor_global_pos + QPoint(0, 2))  # Сдвиг для удобного позиционирования
        #     self.setFixedWidth(200)  # Фиксированная ширина окна подсказок
        #     self.setVisible(True)
        # else:
        #     self.hide()

    def insert_completion(self, item):
        cursor = self.parent().textCursor()

        # Выделяем слово, если курсор находится внутри слова
        cursor.select(cursor.SelectionType.WordUnderCursor)

        # Вставляем подсказку на место курсора (замещаем выбранный текст)
        cursor.insertText(item.text())

        # Перемещаем курсор в конец вставленного текста
        cursor.movePosition(cursor.MoveOperation.Right, cursor.MoveMode.MoveAnchor, n=1)
        self.parent().setTextCursor(cursor)

        # Прячем окно автозаполнения
        self.hide()

    def keyPressEvent(self, event):
        """ Перехватываем клавиши для обработки выбора подсказки """
        super().keyPressEvent(event)

        # Вставка подсказки по нажатию клавиш Enter или Tab
        if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Tab:
            selected_item = self.currentItem()
            if selected_item:
                self.insert_completion(selected_item)

        # Перемещение по подсказкам
        elif event.key() == Qt.Key.Key_Up:
            current_row = self.currentRow()
            if current_row > 0:
                self.setCurrentRow(current_row - 1)

        elif event.key() == Qt.Key.Key_Down:
            current_row = self.currentRow()
            if current_row < self.count() - 1:
                self.setCurrentRow(current_row + 1)

        # Закрытие подсказок при нажатии Esc
        elif event.key() == Qt.Key.Key_Escape:
            self.hide()
        else:
            super().keyPressEvent(event)
