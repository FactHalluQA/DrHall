from loguru import logger

import util
from entity import Question
from util import ChatSlice


def ECMR3_1(question: Question) -> list[ChatSlice]:
    if question.polished_question and question.ECMR3_1:
        return []

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

    logger.bind(question=question, detail='prompt').debug(f'"{chat_slice_1.prompt}"')
    logger.bind(question=question, detail='answer').debug(f'"{chat_slice_1.answer}"')

    chat_slice_2 = util.create_chat_slice(prompt=chat_slice_1.answer)

    logger.bind(question=question, detail='prompt').debug(f'"{chat_slice_2.prompt}"')
    logger.bind(question=question, detail='answer').debug(f'"{chat_slice_2.answer}"')

    return [chat_slice_1, chat_slice_2]
