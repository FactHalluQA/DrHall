# This Python file uses the following encoding: utf-8
import sys

from PyQt6.QtWidgets import QApplication

from qt_main_window_ui import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.setup_ui(widget)
    widget.show()
    sys.exit(app.exec())
