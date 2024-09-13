from concurrent.futures import ThreadPoolExecutor, wait
from time import sleep

from loguru import logger
from translatepy.models import TranslationResult, LanguageResult
from translatepy.translators.google import GoogleTranslateV2

import config
import util
from entity import ExperimentException, Question


def translate_to(text: str,
                 src: str = 'Chinese (Simplified)',
                 dest: str = 'English',
                 verify: bool = True,
                 print_log: bool = True,
                 retry: int = 10) -> tuple[bool, TranslationResult]:
    for _ in range(retry):
        try:
            translation = GoogleTranslateV2().translate(text=text,
                                                        destination_language=dest,
                                                        source_language=src)
            result = True
            if verify:
                result = util.verify_translation(text=text,
                                                 translated_text=translation.result,
                                                 src=src,
                                                 dest=dest)
            if result:
                if print_log:
                    logger.success(f'Successfully translate <{src}>"{text}" to <{dest}>"{translation.result}"')
                return True, translation
            else:
                logger.warning(
                    f'Wrong translation detected! Please check this translation manually! '
                    f'Raw<{src}>"{text}" Translation<{dest}>"{translation.result}"')
                return False, translation
        except Exception as e:
            sleep(0.5)
            logger.warning(
                f'Failed to translate "{text}" to {src}. Retrying... | Exception: {e}')
    raise ExperimentException('Failed to translate! Retry time(s) exceeds allowed time!')


def detect_language(text: str, retry: int = 10) -> LanguageResult:
    for _ in range(retry):
        try:
            detected = GoogleTranslateV2().language(text=text)
            success_hint = f'Successfully detect <{detected.result.name}>"{text}".'
            logger.success(success_hint)
            return detected
        except Exception as e:
            sleep(0.5)
            logger.warning(f'Failed to detect "{text}". Retrying... | Exception: {e}')
    raise ExperimentException('Failed to detect!')


def batch_translate_to_english(questions: list[Question]) -> None:
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(translate_to_english, question=single_question, retry=10)
                   : single_question for single_question in questions
                   if not is_translated(single_question)}
        wait(futures)


def translate_to_english(question: Question, retry: int = 10) -> bool:
    """
    数据集的question（源问题）与answer（正确答案）由中文构造，需将其翻译为英语。
    Parameters
    ----------
    question: 问题
    retry: 重试次数

    Returns
    -------
    """
    result, translation = translate_to(text=question.question_raw, retry=retry)
    if result:
        question.question = translation.result
        return True
    else:
        question.question = f'{config.SYMBOL_GOOGLE_TRANSLATION_FAIL}\nTranslated: [{translation.result}]'
        return False


def is_translated(question: Question) -> bool:
    if not question.question or config.SYMBOL_GOOGLE_TRANSLATION_FAIL in question.question:
        return False
    return True
