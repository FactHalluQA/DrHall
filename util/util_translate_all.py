from concurrent.futures import ThreadPoolExecutor, wait
from typing import List, Dict

from loguru import logger

from entity import Question, QuestionTr
from util import translate_to


def translate_all(question_list: List[Question]) -> List[QuestionTr]:
    question_tr_list: List[QuestionTr] = []
    order = 0
    for question in question_list:
        order += 1
        question_tr = QuestionTr(question_data=question)
        about_to_translate: Dict[str, str] = {}
        for field in question.model_fields:
            attr_in_tr = "tr_" + field
            if (hasattr(question_tr, attr_in_tr) and question.__getattribute__(field)
                    and not question_tr.__getattribute__(attr_in_tr)):
                about_to_translate[attr_in_tr] = question.__getattribute__(field)

        logger.info(f"Translating {order}/{len(question_list)}...")
        try:
            with ThreadPoolExecutor(max_workers=16) as executor:
                futures = {executor.submit(translate_to,
                                           text=text,
                                           src="auto",
                                           dest="Chinese (Simplified)",
                                           verify=False,
                                           print_log=False,
                                           retry=10): key
                           for key, text in about_to_translate.items()}
                wait(futures)
        except Exception as e:
            logger.info(f"Error occurred when translating [{question.sheet_name}][{question.row}]... | Exception: {e}")
            continue

        for future, key in futures.items():
            _, result = future.result()
            setattr(question_tr, key, result.result)
        question_tr_list.append(question_tr)
    return question_tr_list
