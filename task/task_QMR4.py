from loguru import logger

import config
import util
from entity import Question
from util import ChatSlice


def QMR4(question: Question) -> list[ChatSlice]:
    """
    在wiki中搜索实体，并在实体的百科界面查找与源问题中实体相邻的名词或动词。
    将检索到的句子作为证据，构造 Known:【词条名：证据】May I ask:【源问题】的形式。
    Parameters
    ----------
    question: 问题
    """
    if question.QMR4:
        return []

    __fetch_wiki_evidence(question)

    if config.SYMBOL_WIKI_FAIL in question.wiki_evidence:
        return []

    chat_slice = QMR4_step_1(question)

    logger.bind(question=question, detail='prompt').debug(f'"{chat_slice.prompt}"')
    logger.bind(question=question, detail='answer').debug(f'"{chat_slice.answer}"')

    return [chat_slice]


def QMR4_step_1(question: Question, prompt: str = "") -> ChatSlice:
    if not prompt:
        prompt = f"Known:【{question.wiki_evidence}】May I ask:【{question.question}】"
    chat_slice = util.create_chat_slice(prompt=prompt)
    question.QMR4 = chat_slice.answer
    return chat_slice


def __fetch_wiki_evidence(question):
    if not question.wiki_evidence:
        prompt_wiki_evidence = f'Please provide a wiki website link about the answer 【{question.question}】. ' \
                               f'The answer must include a link.'

        logger.bind(question=question, detail='prompt_wiki_evidence').debug(f'"{prompt_wiki_evidence}"')

        bing_answer = util.chat_with_bing(prompt_wiki_evidence).adaptive_text

        logger.bind(question=question, detail='answer_bing').debug(f'"{bing_answer}"')

        titles = util.extract_wiki_titles(bing_answer)
        wiki_evidence = util.merge_wiki_evidence(util.fetch_wiki_evidence(titles=titles)).strip()
        if wiki_evidence:
            question.wiki_evidence = wiki_evidence
        else:
            logger.bind(question=question).warning(r'Failed to find wiki evidence!')
            question.wiki_evidence = config.SYMBOL_WIKI_FAIL
