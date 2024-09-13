from typing import Callable

from ui.qt_question_cell import QuestionCell


class TranslationCell(QuestionCell):
    question_raw: QuestionCell

    def __init__(self,
                 question_raw: QuestionCell,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.question_raw = question_raw

    def handle_function(self, function: Callable):
        text = self.question_raw.text_content.toPlainText()
        if text:
            _, translated_text = function(text)
            self.text_content.setText(translated_text.result)
            self.update()
