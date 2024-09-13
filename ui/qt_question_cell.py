import functools
from typing import Callable, Optional

from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QCoreApplication
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (QGroupBox, QTextEdit, QPushButton, QGridLayout)

import entity
import util
from entity import Question
from util import warn_no_excel_file_chosen


class QuestionCell(QGroupBox):

    def __init__(self,
                 title: str,
                 function_text: Optional[str] = None,
                 function: Optional[Callable] = None,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self._field = None
        self._question = None

        self.setFlat(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font = QFont()
        font.setFamilies([u"Microsoft YaHei"])
        font.setPointSize(12)
        font.setBold(True)

        self.text_content = QTextEdit(self)
        content_font = QFont()
        content_font.setFamilies([u"Microsoft YaHei"])
        content_font.setPointSize(16)
        content_font.setBold(True)
        self.text_content.setFont(content_font)

        self.setFont(font)
        self.setStyleSheet(u"QGroupBox#theBox {border:0;}")
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setFlat(True)

        if function and function_text:
            self.button_function = QPushButton(self)
            self.button_function.setText(function_text)
            self.button_function.setFont(font)
            self.button_function.clicked.connect(functools.partial(self.handle_function, function=function))
        else:
            self.button_function = None
        self.button_save = QPushButton(self)
        self.button_save.setFont(font)
        self.button_save.clicked.connect(self.handle_save)
        self.button_save.setText(u"Save")

        self.layout_grid = QGridLayout(self)
        self.layout_grid.setObjectName("layout_grid")
        self.layout_grid.addWidget(self.text_content, 0, 0, 1, 2)
        self.layout_grid.addWidget(self.button_function, 1, 0, 1, 1)
        self.layout_grid.addWidget(self.button_save, 1, 1, 1, 1)

        self.setTitle(u"{title}".format(title=title))
        self.retranslate_ui()

    @property
    def field(self) -> str:
        return self._field

    @field.setter
    def field(self, value: str) -> None:
        self._field = value

    @property
    def question(self) -> Question:
        return self._question

    @question.setter
    def question(self, value: Question) -> None:
        self._question = value

    @QtCore.pyqtSlot()
    def handle_save(self):
        if self.question:
            sheet_name = self.question.sheet_name
            row = self.question.row
            index = entity.get_real_index_by_field_name(field_name=self.field, headers=self.question.headers)
            content = self.text_content.toPlainText()
            main_window = self.parent().parent()
            util.handle_save(sheet_name, row, index, content, main_window.excel_file)
            main_window.notify_update()
        else:
            warn_no_excel_file_chosen()

    def update_text_content(self, question: Question) -> None:
        super().update()
        self.question = question
        if self.field:
            self.text_content.setText(str(getattr(self.question, self.field)))

    def retranslate_ui(self):
        self.button_save.setText(QCoreApplication.translate("main_window", u"Save", None))
