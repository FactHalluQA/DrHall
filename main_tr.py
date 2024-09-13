from datetime import datetime

from pandas import DataFrame

import config
import main
import util

if __name__ == '__main__':
    sheet_names = main.read_sheets()
    question_list = util.read_excel(sheet_names, path=config.TR_INPUT_PATH)
    question_tr_list = util.translate_all(question_list)
    output_path = config.TR_OUTPUT_PATH.format(time=datetime.now().strftime('%Y-%m-%d_%H-%M-%S_%f'))
    DataFrame([row.__dict__ for row in question_tr_list]).to_excel(output_path)
