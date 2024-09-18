from loguru import logger

import util
from entity import Question
from util import ChatSlice


def QMR2_Dutch(question: Question) -> list[ChatSlice]:
    """
    将源问题分别翻译为西班牙语、德语、荷兰语进行提问，将出现最多的答案作为本方法的答案。
    Parameters
    ----------
    question: 问题
    """
    if question.QMR2_Dutch:
        return []

    chat_slice = QMR2_Dutch_step_1(question)

    logger.bind(question=question, detail='prompt').debug(f'"{chat_slice.prompt}"')
    logger.bind(question=question, detail='answer').debug(f'"{chat_slice.answer}"')

    return [chat_slice]


def QMR2_Dutch_step_1(question: Question, prompt: str = "") -> ChatSlice:
    if not prompt:
        prompt = util.translate_to(question.question, src='English', dest='Dutch', verify=False)[1].result
    chat_slice = util.create_chat_slice(prompt=prompt)
    question.QMR2_Dutch = chat_slice.answer
    return chat_slice
