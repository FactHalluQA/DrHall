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
    # 创建一个DataFrame
    df = DataFrame([row.__dict__ for row in questions])

    # 定义一个重命名映射
    rename_columns = {
        'Source_Answer': 'Source_Answer',
        'QMR1': 'QMR1',
        'QMR2_Spanish': 'QMR2_Spanish',
        'QMR2_German': 'QMR2_German',
        'QMR2_Dutch': 'QMR2_Dutch',
        'QMR3': 'QMR3',
        'QMR4': 'QMR4',
        'AMR1': 'AMR1',
        'AMR2': 'AMR2'
    }

    # 重命名列
    df.rename(columns=rename_columns, inplace=True)

    # 处理可能不存在的列（如果某些列没有数据，上面的重命名将会失败）
    for col in rename_columns.values():
        if col not in df.columns:
            df[col] = None

    output_path = config.OUTPUT_PATH.format(mode=mode, time=datetime.now().strftime('%Y-%m-%d_%H-%M-%S_%f'))
    DataFrame([row.__dict__ for row in questions]).to_excel(output_path)
