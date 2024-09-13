from typing import Callable, Optional

from PyQt6 import QtCore

from entity import Question
from ui.qt_question_cell import QuestionCell
from util import ChatSlice, warn_no_excel_file_chosen


class PromptCell(QuestionCell):
    sibling: "AnswerCell"

    def __init__(self,
                 sibling: Optional["AnswerCell"] = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sibling: "AnswerCell" = sibling


class AnswerCell(QuestionCell):
    sibling: "PromptCell"

    def __init__(self,
                 sibling: Optional["PromptCell"] = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sibling: "PromptCell" = sibling

    @QtCore.pyqtSlot()
    def handle_function(self, function: Callable[[Question, Optional[str]], ChatSlice]):
        if self.question:
            prompt = self.sibling.text_content.toPlainText()
            if prompt:
                chat_slice = function(self.question, prompt)
            else:
                chat_slice = function(self.question)
            self.sibling.text_content.setText(chat_slice.prompt)
            self.text_content.setText(chat_slice.answer)
            self.update()
        else:
            warn_no_excel_file_chosen()
