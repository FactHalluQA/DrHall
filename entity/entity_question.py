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

    '英语': 'english',
    '西班牙语': 'spanish',
    '德语': 'german',
    '荷兰语': 'dutch',

    '重复': 'repeat',
    '一步步思考': 'step_by_step',
    'wiki': 'wiki',
    '这句话不符合事实吗？': 'fact',
    '改造为选择问题': 'reconstruction',

    '重复.1': 'success_repeat',
    '一步步思考.1': 'success_step_by_step',
    '多语言投票': 'success_multilanguage',
    'wiki.1': 'success_wiki',
    '这句话不符合事实吗？.1': 'success_fact',
    '改造为选择问题.1': 'success_reconstruction',

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

    english: str | float = ''
    spanish: str | float = ''
    german: str | float = ''
    dutch: str | float = ''

    repeat: str | float = ''
    step_by_step: str | float = ''
    wiki: str | float = ''
    fact: str | float = ''
    reconstruction: str | float = ''

    success_repeat: str | float = ''
    success_step_by_step: str | float = ''
    success_multilanguage: str | float = ''
    success_wiki: str | float = ''
    success_fact: str | float = ''
    success_reconstruction: str | float = ''
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
