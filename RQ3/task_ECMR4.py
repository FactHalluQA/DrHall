from loguru import logger

import config
import util
from entity import Question
from util import ChatSlice


def ECMR4(question: Question) -> list[ChatSlice]:
    if question.QMR4:
        return []

    if not question.wiki_evidence or config.SYMBOL_WIKI_FAIL in question.wiki_evidence:
        return []

    chat_slice = ECMR4_step_1(question)

    logger.bind(question=question, detail='prompt').debug(f'"{chat_slice.prompt}"')
    logger.bind(question=question, detail='answer').debug(f'"{chat_slice.answer}"')

    return [chat_slice]


def ECMR4_step_1(question: Question, prompt: str = "") -> ChatSlice:
    if not prompt:
        prompt = f"Known:【{question.wiki_evidence}】May I ask:【{question.question}】"
    chat_slice = util.create_chat_slice(prompt=prompt)
    return chat_slice
