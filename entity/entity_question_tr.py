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

    tr_english: str = ''
    tr_spanish: str = ''
    tr_german: str = ''
    tr_dutch: str = ''

    tr_repeat: str = ''
    tr_step_by_step: str = ''
    tr_wiki: str = ''
    tr_fact: str = ''
    tr_reconstruction: str = ''

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
