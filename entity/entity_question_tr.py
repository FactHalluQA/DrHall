from typing import Any

from pydantic import BaseModel

from entity import Question


class QuestionTr(BaseModel):
    class Config:
        exclude = {"question_data"}

    question_data: Question | None = None

    sheet_name: str | int = None
    row: str | int = None

    tr_question_raw: str = ''
    tr_answer_raw: str = ''
    tr_wiki_evidence: str = ''
    tr_Source_Answer: str = ''

    tr_QMR1: str = ''

    tr_QMR2_Spanish: str = ''
    tr_QMR2_German: str = ''
    tr_QMR2_Dutch: str = ''

    tr_QMR3: str = ''

    tr_QMR4: str = ''
    tr_AMR1: str = ''
    tr_AMR2: str = ''

    tr_polished_question: str = ''
    tr_english_phrase: str = ''
    tr_similar_phrases: str = ''
    tr_similar_phrase_1: str = ''
    tr_similar_phrase_2: str = ''

    def __init__(self, question_data: Question, **data: Any):
        super().__init__(**data)
        self.question_data = question_data
        self.sheet_name = question_data.sheet_name
        self.row = question_data.row

        self.tr_question_raw = question_data.question_raw
        self.tr_answer_raw = question_data.answer_raw
