from loguru import logger

import config
import task
import util
from entity import Question

WARNING_NOT_TRANSLATE = r'This is question is not translated properly!'


def handle_question_only(question: Question) -> None:
    try:
        if not util.is_translated(question):
            logger.bind(question=question).warning(WARNING_NOT_TRANSLATE)
            return
        task.answer_in_english(question)
    except Exception as e:
        logger.bind(question=question, detail='question').error(f'Needs to review! | Exception: {e}')


def handle_task_except_english(question: Question) -> None:
    try:
        if not util.is_translated(question):
            logger.bind(question=question).warning(WARNING_NOT_TRANSLATE)
            return
        task.answer_in_spanish(question)
        task.answer_in_german(question)
        task.answer_in_dutch(question)
        task.repeat(question)
        task.step_by_step(question)
        task.fact(question)
        task.reconstruction(question)
    except Exception as e:
        logger.bind(question=question, detail='extra').error(f'Needs to review! | Exception: {e}')


def handle_wiki_only(question: Question) -> None:
    try:
        if not util.is_translated(question):
            logger.bind(question=question).warning(WARNING_NOT_TRANSLATE)
            question.wiki_evidence = config.SYMBOL_WIKI_FAIL
        if config.SYMBOL_WIKI_FAIL not in question.wiki_evidence:
            task.wiki(question)
    except Exception as e:
        logger.bind(question=question, detail='wiki').error(f'Needs to review! | Exception: {e}')


def handle_translated_question(questions: list[Question], mode: str = "question") -> None:
    for item in questions:
        if mode == 'extra':
            task.handle_task_except_english(item)
        elif mode == 'wiki':
            task.handle_wiki_only(item)
        else:
            task.handle_question_only(item)


def mode_question(sheets: list[str], write: bool = True) -> list[Question]:
    questions = util.read_excel(sheet_names=sheets)
    util.batch_translate_to_english(questions)
    handle_translated_question(questions)
    if write:
        util.write_excel(questions, mode='question')
    return questions


def mode_wiki(sheets: list[str], write: bool = True) -> list[Question]:
    questions = util.read_excel(sheet_names=sheets)
    handle_translated_question(questions, mode='wiki')
    if write:
        util.write_excel(questions, mode='wiki')
    return questions


def mode_extra(sheets: list[str], write: bool = True) -> list[Question]:
    questions = util.read_excel(sheet_names=sheets)
    handle_translated_question(questions, mode='extra')
    if write:
        util.write_excel(questions, mode='extra')
    return questions


def mode_full(sheets: list[str], write: bool = True) -> list[Question]:
    questions = mode_question(sheets=sheets, write=False)
    handle_translated_question(questions=questions, mode='wiki')
    handle_translated_question(questions=questions, mode='extra')

    if write:
        util.write_excel(questions, mode='full')
    return questions
