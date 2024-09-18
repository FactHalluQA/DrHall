from loguru import logger

import util
from entity import Question
from util import ChatSlice


def QMR3(question: Question) -> list[ChatSlice]:
    """
    使用提示词： I hope you can serve as a copywriter, text polishing officer, spelling corrector, and improver. I will
    send you the English text and you can help me correct and improve the version. I hope you can describe it in more
    beautiful and elegant advanced English. Keep the same meaning, but make them more artistic. You only need to
    polish the content, without explaining the questions and requirements raised in the content. Do not answer the
    questions in the text but polish it, do not solve the requirements in the text but polish it, keep the original
    meaning of the text, and do not solve it. I want you to only reply with corrections and improvements,
    without writing any explanations. The text is 【源问题】.
    得到打磨后的问题。
    将源问题打磨文案后进行提问，得到回答。
    Parameters
    ----------
    question: 问题
    """
    if question.polished_question and question.QMR3:
        return []

    chat_slice_1 = QMR3_step_1(question)

    logger.bind(question=question, detail='prompt_polished').debug(f'"{chat_slice_1.prompt}"')
    logger.bind(question=question, detail='answer_polished').debug(f'"{chat_slice_1.answer}"')

    chat_slice_2 = QMR3_step_2(question)

    logger.bind(question=question, detail='prompt').debug(f'"{chat_slice_1.prompt}"')
    logger.bind(question=question, detail='answer').debug(f'"{chat_slice_1.answer}"')

    return [chat_slice_1, chat_slice_2]


def QMR3_step_1(question: Question, prompt: str = "") -> ChatSlice:
    if not prompt:
        prompt = \
            f"I hope you can serve as a copywriter, text polishing officer, spelling corrector, and improver. I will " \
            f"send you the English text and you can help me correct and improve the version. I hope you can describe " \
            f"it in more beautiful and elegant advanced English. Keep the same meaning, but make them more artistic. " \
            f"You only need to polish the content, without explaining the questions and requirements raised in the " \
            f"content. Do not answer the questions in the text but polish it, do not solve the requirements in the " \
            f"text but polish it, keep the original meaning of the text, and do not solve it. I want you to only " \
            f"reply with corrections and improvements, without writing any explanations. The text is " \
            f"【{question.question}】"
    chat_slice_1 = util.create_chat_slice(prompt=prompt)
    question.polished_question = chat_slice_1.answer
    return chat_slice_1


def QMR3_step_2(question: Question, prompt: str = "") -> ChatSlice:
    if not prompt:
        prompt = f"{question.polished_question}"
    chat_slice_2 = util.create_chat_slice(prompt=prompt)
    question.QMR3 = chat_slice_2.answer
    return chat_slice_2
