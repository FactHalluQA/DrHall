from typing import Callable, Any

from PyQt6 import QtCore
from PyQt6.QtWidgets import (QGroupBox, QPushButton, QTextEdit, QGridLayout)

from entity import Question


class QuestionCell(QGroupBox):
    def __init__(self,
                 title: str = ...,
                 function_text: str | None = ...,
                 function: Callable[[Question], Any] | None = ...,
                 *args,
                 **kwargs) -> None: ...

    @property
    def field(self) -> str: ...

    @property
    def question(self) -> Question: ...

    @QtCore.pyqtSlot()
    def handle_function(self, function: Callable): ...

    @QtCore.pyqtSlot()
    def handle_save(self): ...

    def retranslate_ui(self): ...

    def update_text_content(self, question: Question) -> None: ...

    layout_grid: QGridLayout
    text_content: QTextEdit
    button_function: QPushButton | None
    button_save: QPushButton

    field: str
    question: Question
