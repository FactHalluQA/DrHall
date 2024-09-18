from loguru import logger

import util
from entity import Question
from util import ChatSlice


def ECMR2_3(question: Question) -> list[ChatSlice]:
    chat_slice = ECMR2_3_step_1(question)

    logger.bind(question=question, detail='prompt').debug(f'"{chat_slice.prompt}"')
    logger.bind(question=question, detail='answer').debug(f'"{chat_slice.answer}"')

    return [chat_slice]


def ECMR2_3_step_1(question: Question, prompt: str = "") -> ChatSlice:
    if not prompt:
        prompt = f"【{question.question} {question.Source_Answer}】Please analyze this sentence based on the presence or absence of errors."
    chat_slice = util.create_chat_slice(prompt=prompt)
    return chat_slice
