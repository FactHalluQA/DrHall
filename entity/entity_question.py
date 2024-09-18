import re
from typing import Any, Tuple, Union

from openpyxl.cell import Cell
from pydantic import BaseModel

# 标题和属性的映射
HEADER_MAP = {
    'question_raw': 'question_raw',
    'answer_raw': 'answer_raw',
    'question': 'question',
    'wiki_evidence': 'wiki_evidence',
    'Source_Answer': 'Source_Answer',

    'QMR1': 'QMR1',

    'QMR2_Spanish': 'QMR2_Spanish',
    'QMR2_German': 'QMR2_German',
    'QMR2_Dutch': 'QMR2_Dutch',

    'QMR3': 'QMR3',

    'QMR4': 'QMR4',

    'AMR1': 'AMR1',
    'AMR2': 'AMR2',

    'Consistency_QMR1': 'Consistency_QMR1',
    'Consistency_QMR2': 'Consistency_QMR2',
    'Consistency_QMR3': 'Consistency_QMR3',
    'Consistency_QMR4': 'Consistency_QMR4',
    'Consistency_AMR1': 'Consistency_AMR1',
    'Consistency_AMR2': 'Consistency_AMR2',

    'polished_question': 'polished_question',
    'english_phrase': 'english_phrase',
    'similar_phrases': 'similar_phrases',
    'similar_phrase_1': 'similar_phrase_1',
    'similar_phrase_2': 'similar_phrase_2'
}


def get_field_name_by_real_name(real_name: str) -> str:
    return HEADER_MAP[real_name]


def get_real_name_by_field_name(field_name: str) -> str:
    return {v: k for k, v in HEADER_MAP.items()}[field_name]


def get_real_index_by_field_name(field_name: str, headers: Tuple[Cell]) -> int:
    real_name = get_real_name_by_field_name(field_name)
    jump_time = 0
    if real_name.endswith(".1"):
        jump_time = 1
    for index, header in enumerate(headers):
        name_in_excel: str = header.value
        if name_in_excel == real_name:
            if re.match(r".*\.\d+$", name_in_excel):
                return index
            if jump_time:
                jump_time -= 1
            else:
                return index
    return -1


class Question(BaseModel):
    class Config:
        exclude = {"headers", "_headers"}

    # Data
    question_raw: str | float = ''
    answer_raw: str | float = ''
    question: str | float = ''
    wiki_evidence: str | float = ''
    Source_Answer: str | float = ''

    QMR1: str | float = ''
    QMR2_Spanish: str | float = ''
    QMR2_Dutch: str | float = ''
    QMR2_German: str | float = ''
    QMR3: str | float = ''
    QMR4: str | float = ''
    AMR1: str | float = ''
    AMR2: str | float = ''

    Consistency_QMR1: str | float = ''
    Consistency_QMR2_Dutch: str | float = ''
    Consistency_QMR2_German: str | float = ''
    Consistency_QMR2_Spanish: str | float = ''
    Consistency_QMR3: str | float = ''
    Consistency_QMR4: str | float = ''
    Consistency_AMR1: str | float = ''
    Consistency_AMR2: str | float = ''

    # Intermedia
    polished_question: str = ''
    english_phrase: str = ''
    similar_phrases: str = ''
    similar_phrase_1: str = ''
    similar_phrase_2: str = ''
    # Position information
    sheet_name: str | int = None
    row: str | int = None

    def __init__(self, sheet_name: str | int, row: str | int, **data: Any):
        super().__init__(**data)
        self.sheet_name = sheet_name
        self.row = row
        self._headers = None

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        self._headers = value

    @headers.deleter
    def headers(self):
        del self._headers

    @staticmethod
    def from_rows(sheet_name: str, headers: Tuple[Cell, ...], rows: Union[Tuple[Cell, ...], Tuple[Tuple, ...]]) \
            -> list["Question"]:
        if isinstance(rows[0], Tuple):
            question_list = []
            for item in rows:
                question_list.extend(Question.from_rows(sheet_name, headers, item))
            return question_list
        else:
            question = Question(sheet_name=sheet_name, row=rows[0].row)
            for i in range(len(headers)):
                header = headers[i].value
                if header in HEADER_MAP.keys():
                    property_name = HEADER_MAP[header]
                    # 属性存在同名情况，后者会覆盖前者
                    if getattr(question, property_name):
                        property_name = HEADER_MAP[header + '.1']
                    value = rows[i].value
                    if value:
                        setattr(question, property_name, value)
                    else:
                        setattr(question, property_name, "")

            question.headers = headers
            return [question]
