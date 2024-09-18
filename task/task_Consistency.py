from loguru import logger

import util
from entity import Question
from util import ChatSlice


def Consistency(question: Question) -> list[ChatSlice]:
    """
    Question：【源问题】
    Answer1：【回答1】
    Answer2：【回答2】
    Are the above two answers to the question consistent? Please answer in as few words or phrases as possible. Do not evaluate the rightness or wrongness of the answer itself. Note: Yes and right have the same meaning; No and Wrong have the same meaning.

    一致性评估，调用GPT3.5，自动化评估后续回答与源回答是否一致。

    Parameters
    ----------
    question: 问题
    """
    if question.consistency:
        return []

    chat_slice_1 = Consistency_step_1(question)

    logger.bind(question=question, detail='prompt').debug(f'"{chat_slice_1.prompt}"')
    logger.bind(question=question, detail='answer').debug(f'"{chat_slice_1.answer}"')

    chat_slice_2 = Consistency_step_2(question)

    logger.bind(question=question, detail='prompt').debug(f'"{chat_slice_2.prompt}"')
    logger.bind(question=question, detail='answer').debug(f'"{chat_slice_2.answer}"')

    chat_slice_3 = Consistency_step_3(question)

    logger.bind(question=question, detail='prompt').debug(f'"{chat_slice_3.prompt}"')
    logger.bind(question=question, detail='answer').debug(f'"{chat_slice_3.answer}"')

    chat_slice_4 = Consistency_step_4(question)

    logger.bind(question=question, detail='prompt').debug(f'"{chat_slice_4.prompt}"')
    logger.bind(question=question, detail='answer').debug(f'"{chat_slice_4.answer}"')

    chat_slice_5 = Consistency_step_5(question)

    logger.bind(question=question, detail='prompt').debug(f'"{chat_slice_5.prompt}"')
    logger.bind(question=question, detail='answer').debug(f'"{chat_slice_5.answer}"')

    chat_slice_6 = Consistency_step_6(question)

    logger.bind(question=question, detail='prompt').debug(f'"{chat_slice_6.prompt}"')
    logger.bind(question=question, detail='answer').debug(f'"{chat_slice_6.answer}"')

    chat_slice_7 = Consistency_step_7(question)

    logger.bind(question=question, detail='prompt').debug(f'"{chat_slice_7.prompt}"')
    logger.bind(question=question, detail='answer').debug(f'"{chat_slice_7.answer}"')

    chat_slice_8 = Consistency_step_8(question)

    logger.bind(question=question, detail='prompt').debug(f'"{chat_slice_8.prompt}"')
    logger.bind(question=question, detail='answer').debug(f'"{chat_slice_8.answer}"')

    return [chat_slice_1,
            chat_slice_2,
            chat_slice_3,
            chat_slice_4,
            chat_slice_5,
            chat_slice_6,
            chat_slice_7,
            chat_slice_8, ]


def Consistency_step_1(question: Question, prompt: str = "") -> ChatSlice:
    if not prompt:
        prompt = \
            (f"Question：【{question.question}】"
             f"Answer1：【{question.Source_Answer}】"
             f"Answer2：【{question.QMR1}】"
             f"Are the above two answers to the question consistent? Please answer in as few words or phrases as possible. Do not evaluate the rightness or wrongness of the answer itself. Note: Yes and right have the same meaning; No and Wrong have the same meaning.")
    chat_slice = util.create_chat_slice(prompt=prompt)
    question.Consistency_QMR1 = chat_slice.answer
    return chat_slice


def Consistency_step_2(question: Question, prompt: str = "") -> ChatSlice:
    if not prompt:
        prompt = \
            (f"Question：【{question.question}】"
             f"Answer1：【{question.Source_Answer}】"
             f"Answer2：【{question.QMR2_Dutch}】"
             f"Are the above two answers to the question consistent? Please answer in as few words or phrases as possible. Do not evaluate the rightness or wrongness of the answer itself. Note: Yes and right have the same meaning; No and Wrong have the same meaning.")
    chat_slice = util.create_chat_slice(prompt=prompt)
    question.Consistency_QMR2_Dutch = chat_slice.answer
    return chat_slice


def Consistency_step_3(question: Question, prompt: str = "") -> ChatSlice:
    if not prompt:
        prompt = \
            (f"Question：【{question.question}】"
             f"Answer1：【{question.Source_Answer}】"
             f"Answer2：【{question.QMR2_German}】"
             f"Are the above two answers to the question consistent? Please answer in as few words or phrases as possible. Do not evaluate the rightness or wrongness of the answer itself. Note: Yes and right have the same meaning; No and Wrong have the same meaning.")
    chat_slice = util.create_chat_slice(prompt=prompt)
    question.Consistency_QMR2_German = chat_slice.answer
    return chat_slice


def Consistency_step_4(question: Question, prompt: str = "") -> ChatSlice:
    if not prompt:
        prompt = \
            (f"Question：【{question.question}】"
             f"Answer1：【{question.Source_Answer}】"
             f"Answer2：【{question.QMR2_Spanish}】"
             f"Are the above two answers to the question consistent? Please answer in as few words or phrases as possible. Do not evaluate the rightness or wrongness of the answer itself. Note: Yes and right have the same meaning; No and Wrong have the same meaning.")
    chat_slice = util.create_chat_slice(prompt=prompt)
    question.Consistency_QMR2_Spanish = chat_slice.answer
    return chat_slice


def Consistency_step_5(question: Question, prompt: str = "") -> ChatSlice:
    if not prompt:
        prompt = \
            (f"Question：【{question.question}】"
             f"Answer1：【{question.Source_Answer}】"
             f"Answer2：【{question.QMR3}】"
             f"Are the above two answers to the question consistent? Please answer in as few words or phrases as possible. Do not evaluate the rightness or wrongness of the answer itself. Note: Yes and right have the same meaning; No and Wrong have the same meaning.")
    chat_slice = util.create_chat_slice(prompt=prompt)
    question.Consistency_QMR3 = chat_slice.answer
    return chat_slice


def Consistency_step_6(question: Question, prompt: str = "") -> ChatSlice:
    if not prompt:
        prompt = \
            (f"Question：【{question.question}】"
             f"Answer1：【{question.Source_Answer}】"
             f"Answer2：【{question.QMR4}】"
             f"Are the above two answers to the question consistent? Please answer in as few words or phrases as possible. Do not evaluate the rightness or wrongness of the answer itself. Note: Yes and right have the same meaning; No and Wrong have the same meaning.")
    chat_slice = util.create_chat_slice(prompt=prompt)
    question.Consistency_QMR4 = chat_slice.answer
    return chat_slice


def Consistency_step_7(question: Question, prompt: str = "") -> ChatSlice:
    if not prompt:
        prompt = \
            (f"Question：【{question.question}】"
             f"Answer1：【{question.Source_Answer}】"
             f"Answer2：【{question.AMR1}】"
             f"Are the above two answers to the question consistent? Please answer in as few words or phrases as possible. Do not evaluate the rightness or wrongness of the answer itself. Note: Yes and right have the same meaning; No and Wrong have the same meaning.")
    chat_slice = util.create_chat_slice(prompt=prompt)
    question.Consistency_AMR1 = chat_slice.answer
    return chat_slice


def Consistency_step_8(question: Question, prompt: str = "") -> ChatSlice:
    if not prompt:
        prompt = \
            (f"Question：【{question.question}】"
             f"Answer1：【{question.Source_Answer}】"
             f"Answer2：【{question.AMR2}】"
             f"Are the above two answers to the question consistent? Please answer in as few words or phrases as possible. Do not evaluate the rightness or wrongness of the answer itself. Note: Yes and right have the same meaning; No and Wrong have the same meaning.")
    chat_slice = util.create_chat_slice(prompt=prompt)
    question.Consistency_AMR2 = chat_slice.answer
    return chat_slice
