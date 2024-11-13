class Logger:
    def __init__(self, console_widget=None):
        self.console_widget = console_widget

    def log(self, message):
        if self.console_widget:
            self.console_widget.append_log(message)
        print(message)  # Вывод в консоль