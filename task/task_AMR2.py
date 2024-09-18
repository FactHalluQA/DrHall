from loguru import logger

import util
from entity import Question, ExperimentException
from util import ChatSlice


def AMR2(question: Question) -> list[ChatSlice]:
    """
    Question：【源问题】
    Answer：【源回答】
    Try to summarize the answer into one word or one phrase.
    得到源回答（短语）

    询问chatgpt查询源回答（短语）的近义词。
    Please provide two phrases similar to “源回答（短语）”
    Note: Similar words should have a different meaning. I want you to only reply with similar words, without writing
    any explanations.
    得到近义词1、2。

    构造 源问题是“源回答”还是“近义词1”还是“近义词2”？又或者以上提到的选项都不正确？ 的形式。

    Parameters
    ----------
    question: 问题
    """
    if question.english_phrase and question.similar_phrases and question.AMR2:
        return []

    chat_slice_1 = AMR2_step_1(question)

    logger.bind(question=question, detail='prompt_get_english_phase_form').debug(f'"{chat_slice_1.prompt}"')
    logger.bind(question=question, detail='english_phrase').debug(f'"{question.english_phrase}"')

    chat_slice_2 = AMR2_step_2(question)

    logger.bind(question=question, detail='prompt_get_similar_phases').debug(f'"{chat_slice_2.prompt}"')
    logger.bind(question=question, detail='similar_phrases').debug(f'"{question.similar_phrases}"')
    try:
        question.similar_phrase_1, question.similar_phrase_2 = __split_answer(question.similar_phrases)
    except ExperimentException:
        logger.bind(question=question, detail='split') \
            .warning(r"Failed to figure out similar answers. Please pay attention to this!")
        return []

    chat_slice_3 = AMR2_step_3(question)

    logger.bind(question=question, detail='prompt').debug(f'"{chat_slice_3.prompt}"')
    logger.bind(question=question, detail='answer').debug(f'"{question.AMR2}"')

    return [chat_slice_1, chat_slice_2, chat_slice_3]


def AMR2_step_1(question: Question, prompt: str = "") -> ChatSlice:
    if not prompt:
        prompt = \
            (f"Question：【{question.question}】 Answer：【{question.Source_Answer}】 "
             f"Try to summarize the answer into one word or one phrase. "
             f"Please be as concise as possible.")
    chat_slice_1 = util.create_chat_slice(prompt=prompt)
    question.english_phrase = chat_slice_1.answer
    return chat_slice_1


def AMR2_step_2(question: Question, prompt: str = "") -> ChatSlice:
    if not prompt:
        prompt = \
            (f"Please provide two phrases similar to 【{question.english_phrase}】 "
             f"Note: Similar words should have different meanings. "
             f"I want you to only reply with similar terms, without writing any explanations. "
             f"Number them with series, and split them with a line break."
             f"Do not include original answer.")
    chat_slice_2 = util.create_chat_slice(prompt=prompt)
    question.similar_phrases = chat_slice_2.answer
    return chat_slice_2


def AMR2_step_3(question: Question, prompt: str = "") -> ChatSlice:
    if not prompt:
        prompt = \
            (f"The answer of question 【{question.question}】 is 【{question.english_phrase}】 or "
             f"【{question.similar_phrase_1}】, or【{question.similar_phrase_2}】? "
             f"Or none of the above?")
    chat_slice_3 = util.create_chat_slice(prompt=prompt)
    question.AMR2 = chat_slice_3.answer
    return chat_slice_3


def __split_answer(similar_phrases):
    split_characters = ['\n', ',']
    split_character = ''
    for character in split_characters:
        if character in similar_phrases:
            split_character = character
            answers = similar_phrases.strip().split(split_character)
            return answers[0].replace('1. ', '', 1), answers[1].replace('2. ', '', 1)
    raise ExperimentException(f"Failed to split answer {split_character}!")
