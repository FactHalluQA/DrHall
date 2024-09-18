from loguru import logger

import util
from entity import Question
from util import ChatSlice


def QMR1(question: Question) -> list[ChatSlice]:
    """
    在源问题后加入提示词：Please think step by step.
    构造：源问题.Please think step by step.
    进行提问，得到回答。判断此方法是否成功进行了事实验证。
    Parameters
    ----------
    question: 问题
    """
    if question.QMR1:
        return []

    chat_slice = QMR1_step_1(question)

    logger.bind(question=question, detail='prompt').debug(f'"{chat_slice.prompt}"')
    logger.bind(question=question, detail='answer').debug(f'"{chat_slice.answer}"')

    return [chat_slice]


def QMR1_step_1(question: Question, prompt: str = "") -> ChatSlice:
    if not prompt:
        prompt = f'【{question.question}】Please think step by step.'
    chat_slice = util.create_chat_slice(prompt=prompt)
    question.QMR1 = chat_slice.answer
    return chat_slice
