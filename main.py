import argparse
import sys

import openpyxl
from loguru import logger
from openpyxl.workbook import Workbook

import config
from entity import Question
from task import common

argParser = argparse.ArgumentParser()
argParser.add_argument("-m", "--mode", type=str, nargs='?', default='question',
                       help="Default mode is answer question in English only. "
                            "'--mode=wiki' if you want to handle wiki tasks. "
                            "'--mode=extra' if you want to handle extra tasks."
                            "'--mode=consistency' if you want to handle consistency tasks.")
argParser.add_argument("-l", "--log", type=str, nargs='?', default='on',
                       help="Default logging is on and records are stored in 'logs' folder. "
                            "'--log=off' if you do need logs. (I do not recommend this.)")
argParser.add_argument("-M", "--model", type=int, nargs='?', default=1,
                       help="Switch ChatGPT's model. See detailed meanings of the numbers in `config.py` "
                            "Default model is `gpt-3.5-turbo`.)")


def read_sheets() -> list[str]:
    sheet_names: list[str | int] = []
    while True:
        input_value = input("Input the sheet names or indices. End with blank line:\n")
        if input_value.strip():
            sheet_names.append(input_value)
        else:
            break
    if not sheet_names:
        logger.error("Empty input!")
        exit()
    workbook: Workbook = openpyxl.load_workbook(config.INPUT_PATH)
    available_sheet_names: list[str] = workbook.sheetnames
    needed_sheet_names: list[str] = []
    for name in sheet_names:
        try:
            index = int(name)
            if (0 < index <= len(available_sheet_names)) and \
                    (available_sheet_names[index - 1] not in needed_sheet_names):
                needed_sheet_names.append(available_sheet_names[index - 1])
        except ValueError:
            if (name in available_sheet_names) and (name not in needed_sheet_names):
                needed_sheet_names.append(name)
    return needed_sheet_names


if __name__ == '__main__':
    args: argparse.Namespace = argParser.parse_args()
    logger_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<white>[{extra[question].sheet_name}][{extra[question].row}][{function}][{extra[detail]}]</white> | "
        "{message}"
    )
    logger.remove()
    logger.add(sys.stderr, format=logger_format)
    logger.configure(extra={"question": Question(-1, -1), "detail": ''})
    if str(args.log).lower() != 'off':
        logger.add("logs/file_{time}.log", format=logger_format, rotation="10 MB")

    config.GPT_MODEL = args.model

    sheets = read_sheets()
    logger.success(f"Reading sheets: {str(sheets)}")
    if str(args.mode).lower() == 'extra':
        common.mode_extra(sheets)
    elif str(args.mode).lower() == 'wiki':
        common.mode_wiki(sheets)
    elif str(args.mode).lower() == 'full':
        common.mode_full(sheets)
    elif str(args.mode).lower() == 'consistency':
        common.mode_consistency(sheets)
    else:
        common.mode_question(sheets)
