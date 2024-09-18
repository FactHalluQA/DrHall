from loguru import logger

import util
from entity import Question
from util import ChatSlice


def Source_Answer(question: Question) -> list[ChatSlice]:
    """
    向ChatGPT提问英语问题，得到答案作为源答案。

    2023-07-13
    曹：生成源回答的时候加个提示“尽量短地生成回答”，以减少答案长度。（可使用提示词【】Please try to answer in one sentence.简化答案生成
    为一个句子）
    Parameters
    ----------
    question: 问题
    """
    if question.Source_Answer:
        return []

    chat_slice = Source_Answer_step_1(question)

    logger.bind(question=question, detail='prompt').debug(f'"{chat_slice.prompt}"')
    logger.bind(question=question, detail='answer').debug(f'"{chat_slice.answer}"')

    return [chat_slice]


def Source_Answer_step_1(question: Question, prompt: str = "") -> ChatSlice:
    if not prompt:
        prompt = f'【{question.question}】Please try to answer in one sentence.'
    chat_slice = util.create_chat_slice(prompt)
    question.Source_Answer = chat_slice.answer
    return chat_slice
