from loguru import logger

import util
from entity import Question
from util import ChatSlice


def ECMR2_3(question: Question) -> list[ChatSlice]:
    if question.QMR2_Spanish:
        return []

    chat_slice = ECMR2_3_step_1(question)

    logger.bind(question=question, detail='prompt').debug(f'"{chat_slice.prompt}"')
    logger.bind(question=question, detail='answer').debug(f'"{chat_slice.answer}"')

    return [chat_slice]


def ECMR2_3_step_1(question: Question, prompt: str = "") -> ChatSlice:
    if not prompt:
        prompt = util.translate_to(question.question, src='English', dest='Spanish', verify=False)[1].result
    chat_slice = util.create_chat_slice(prompt=prompt)
    return chat_slice
