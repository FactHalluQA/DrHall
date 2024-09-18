from loguru import logger

import util
from entity import Question
from util import ChatSlice


def AMR1(question: Question) -> list[ChatSlice]:
    """
    在源回答（句子）后加入提示“Is this statement not true?”，构造：【源回答】，Is this statement not true?的格式。 输出的答案若不符合事实则检出错误。 注意：not
    accurate或not true不一定真错误，输出的答案需看后面的解释。解释过于离谱可以多问几次（选错可能是概率问题，多问几次可能就选对了）。若回答为“部分准确”，也认为是符合事实（该方法有可能诱导chatgpt
    故意挑错，部分正确可以相当于全部正确）。
    Parameters
    ----------
    question: 问题
    """
    if question.AMR1:
        return []

    chat_slice = AMR1_step_1(question)

    logger.bind(question=question, detail='prompt').debug(f'"{chat_slice.prompt}"')
    logger.bind(question=question, detail='answer').debug(f'"{chat_slice.answer}"')

    return [chat_slice]


def AMR1_step_1(question: Question, prompt: str = "") -> ChatSlice:
    if not prompt:
        prompt = f"【{question.question} {question.Source_Answer}】, is this statement not true?"
    chat_slice = util.create_chat_slice(prompt=prompt)
    question.AMR1 = chat_slice.answer
    return chat_slice
