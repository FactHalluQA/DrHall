from typing import Callable

from loguru import logger

import util
from entity import AIModel, ExperimentException


def __chat_with_model(model: AIModel) -> Callable:
    if model == AIModel.ChatGPT:
        return util.chat_with_chatgpt
    if model == AIModel.ChatGPTLegacy:
        return util.chat_with_chatgpt_legacy
    if model == AIModel.Bard:
        return util.chat_with_bard
    raise ExperimentException(r'Unsupported AI Model!')


def verify_sentence(string: str, model: AIModel = AIModel.ChatGPT) -> bool:
    """
    Check if a `string` is a sentence.
    """
    prompt = f'Is 【{string}】 an intact sentence? Please answer me by yes or no.'

    logger.bind(detail='prompt').debug(prompt)

    contents = __chat_with_model(model)(prompt)

    logger.bind(detail='answer').debug(str(contents))

    counts = {'yes': 0, 'no': 0}
    for content in contents:
        if content.lower().startswith('yes'):
            counts['yes'] += 1
        else:
            counts['no'] += 1
    return counts['yes'] > counts['no']


def verify_translation(text: str,
                       translated_text: str,
                       src: str = 'Chinese (Simplified)',
                       dest: str = 'English',
                       model: AIModel = AIModel.ChatGPT) -> bool:
    """
    验证Google翻译的正确性。
    Parameters
    ----------
    text 源文本
    translated_text 翻译文本
    src 源语言
    dest 目标语言

    Returns
    -------
    翻译正确与否
    """
    prompt = f"Known its original sentence 【{text}】 in 【{src}】, is its " \
             f"translation 【{translated_text}】 correct in 【{dest}】? " \
             f"Answer me by yes or no."
    logger.bind(detail='prompt').debug(f'"{prompt}"')
    answer = str(__chat_with_model(model)(prompt)).lower()
    logger.bind(detail='answer').debug(f'"{answer}"')
    return 'yes' in answer
