from datetime import datetime

import openpyxl
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from pandas import DataFrame

import config
from entity import Question


def read_excel(sheet_names: list[str], path=config.INPUT_PATH) -> list[Question]:
    workbook: Workbook = openpyxl.load_workbook(path)
    header_cells = workbook.active[1]
    all_questions = []
    for sheet_name in sheet_names:
        worksheet: Worksheet = workbook[sheet_name]
        for i in range(2, worksheet.max_row):
            all_questions.extend(Question.from_rows(sheet_name, header_cells, worksheet[i]))

    return all_questions


def write_excel(questions: list[Question], mode: str = 'question') -> None:
    output_path = config.OUTPUT_PATH.format(mode=mode, time=datetime.now().strftime('%Y-%m-%d_%H-%M-%S_%f'))
    DataFrame([row.__dict__ for row in questions]).to_excel(output_path)
