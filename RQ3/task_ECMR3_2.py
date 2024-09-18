from loguru import logger

import util
from entity import Question
from util import ChatSlice


def ECMR3_2(question: Question) -> list[ChatSlice]:
    if question.polished_question and question.ECMR3_1:
        return []

    prompt = \
        (f"I hope you can serve as a copywriter, text polishing officer. I will send you the English text and you can "
         f"help me improve the version. I hope you can describe it in some other, more appropriate sentence "
         f"structure, provided you change the words as little as possible. Keep the same meaning, but make them "
         f"easier to be understood. You only need to polish the content, without explaining the questions and "
         f"requirements raised in the content. Do not answer the questions in the text but polish it, do not solve "
         f"the requirements in the text but polish it, keep the original meaning of the text, and do not solve it. I "
         f"want you to only reply with corrections and improvements, without writing any explanations."
         f"The text is【{question.question}】")

    chat_slice_1 = util.create_chat_slice(prompt=prompt)

    logger.bind(question=question, detail='prompt').debug(f'"{chat_slice_1.prompt}"')
    logger.bind(question=question, detail='answer').debug(f'"{chat_slice_1.answer}"')

    chat_slice_2 = util.create_chat_slice(prompt=chat_slice_1.answer)

    logger.bind(question=question, detail='prompt').debug(f'"{chat_slice_2.prompt}"')
    logger.bind(question=question, detail='answer').debug(f'"{chat_slice_2.answer}"')

    return [chat_slice_1, chat_slice_2]
