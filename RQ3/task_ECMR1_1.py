from loguru import logger

import util
from entity import Question
from util import ChatSlice


def ECMR2_2(question: Question) -> list[ChatSlice]:
    chat_slice = ECMR2_2_step_1(question)

    logger.bind(question=question, detail='prompt').debug(f'"{chat_slice.prompt}"')
    logger.bind(question=question, detail='answer').debug(f'"{chat_slice.answer}"')

    return [chat_slice]


def ECMR2_2_step_1(question: Question, prompt: str = "") -> ChatSlice:
    if not prompt:
        prompt = f"【{question.question} {question.Source_Answer}】, is this statement true?"
    chat_slice = util.create_chat_slice(prompt=prompt)
    return chat_slice
