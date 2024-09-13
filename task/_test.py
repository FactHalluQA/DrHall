import sys
import unittest

from loguru import logger

import task
import util
from entity import Question

COMMON_QUESTION = "In which year was Galileo's \"Dialogue between Two New Sciences\" published?"
COMMON_ANSWER = "1638"

COMMON_QUESTION_CHINESE = "粒径500纳米和10微米的钨粉末，哪种更容易在高温下烧结成致密块体？"
COMMON_ANSWER_CHINESE = "粒径500纳米"

COMMON_QUESTION_EXAMPLE = Question('', '')
COMMON_QUESTION_EXAMPLE.question = COMMON_QUESTION
COMMON_QUESTION_EXAMPLE.answer_raw = COMMON_ANSWER

COMMON_QUESTION_EXAMPLE_CHINESE = Question('', '')
COMMON_QUESTION_EXAMPLE_CHINESE.question_raw = COMMON_QUESTION_CHINESE
COMMON_QUESTION_EXAMPLE_CHINESE.answer_raw = COMMON_ANSWER_CHINESE

logger_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<white>[{extra[question].sheet_name}][{extra[question].row}][{function}][{extra[detail]}]</white> | "
    "{message}"
)
logger.remove()
logger.add(sys.stderr, format=logger_format)
logger.configure(extra={"question": Question(-1, -1), "detail": ''})


def _read() -> list[Question]:
    return util.read_excel(["物理wh"])


def simple_detect(text: str) -> str:
    return util.detect_language(text.strip()).result.name


class TestDummy(unittest.TestCase):
    def test_verify_chatgpt_api_keys(self):
        util.verify_chatgpt_api_keys()

    def test_get_models(self):
        models = util.get_models()
        model_names = []
        for model in models.data:
            model_names.append(model.id)
        model_names = sorted(set(model_names))
        for model_name in model_names:
            logger.success(model_name)


class TestChatGPT(unittest.TestCase):
    def test_verify_translation(self):
        self.assertTrue(util.verify_translation('珠穆朗玛峰是世界上最高的山峰。',
                                                'Mount Everest is the tallest mountain in the world.',
                                                'Chinese (Simplified)',
                                                'English'))
        self.assertFalse(util.verify_translation('珠穆朗玛峰是世界上最高的山峰。',
                                                 'I love you!',
                                                 'Chinese (Simplified)',
                                                 'English'))

    def test_a_chat_with_chatgpt(self):
        response = util.chat_with_chatgpt("I love you!")
        logger.success(response)
        self.assertTrue(response)

    def test_b_answer_in_english(self):
        task.answer_in_english(COMMON_QUESTION_EXAMPLE)
        logger.success(COMMON_QUESTION_EXAMPLE.english.strip())
        self.assertEqual(simple_detect(COMMON_QUESTION_EXAMPLE.english), 'English')

    def test_c_answer_in_spanish(self):
        task.answer_in_spanish(COMMON_QUESTION_EXAMPLE)
        logger.success(COMMON_QUESTION_EXAMPLE.spanish.strip())
        self.assertEqual(simple_detect(COMMON_QUESTION_EXAMPLE.spanish), 'Spanish')

    def test_d_answer_in_germany(self):
        task.answer_in_german(COMMON_QUESTION_EXAMPLE)
        logger.success(COMMON_QUESTION_EXAMPLE.german.strip())
        self.assertEqual(simple_detect(COMMON_QUESTION_EXAMPLE.german), 'German')

    def test_e_answer_in_dutch(self):
        task.answer_in_dutch(COMMON_QUESTION_EXAMPLE)
        logger.success(COMMON_QUESTION_EXAMPLE.dutch.strip())
        self.assertEqual(simple_detect(COMMON_QUESTION_EXAMPLE.dutch), 'Dutch')

    def test_f_repeat(self):
        task.repeat(COMMON_QUESTION_EXAMPLE)
        self.assertTrue(COMMON_QUESTION_EXAMPLE.repeat)

    def test_g_step_by_step(self):
        task.step_by_step(COMMON_QUESTION_EXAMPLE)
        self.assertTrue(COMMON_QUESTION_EXAMPLE.step_by_step)

    def test_h_wiki(self):
        task.wiki(COMMON_QUESTION_EXAMPLE)
        self.assertTrue(COMMON_QUESTION_EXAMPLE.wiki)

    def test_i_fact(self):
        task.answer_in_english(COMMON_QUESTION_EXAMPLE)
        task.fact(COMMON_QUESTION_EXAMPLE)
        self.assertTrue(COMMON_QUESTION_EXAMPLE.fact)

    def test_j_reconstruction(self):
        task.answer_in_english(COMMON_QUESTION_EXAMPLE)
        task.reconstruction(COMMON_QUESTION_EXAMPLE)
        self.assertTrue(COMMON_QUESTION_EXAMPLE.reconstruction)


class TestBard(unittest.TestCase):
    def test_chat_with_bard(self):
        util.chat_with_bard('I love you!')

    def test_verify_sentence(self):
        bard_yes = "I love Chinese food."
        self.assertTrue(util.verify_sentence(bard_yes))
        bard_no = "Chinese food."
        self.assertFalse(util.verify_sentence(bard_no))


class TestBing(unittest.TestCase):
    def test_chat_with_bing(self):
        response = util.chat_with_bing('I love you!')
        logger.success(response)
        self.assertTrue(response)


class TestGoogleTranslation(unittest.TestCase):
    def test_translate_to(self):
        question_raw = '英国物理学家托马斯·杨成功地观察到了光的什么现象？'
        translation = util.translate_to(question_raw)
        self.assertFalse(translation)

        question_raw = '折射定律是由谁发现的？'
        translation = util.translate_to(question_raw)
        self.assertTrue(translation)

    def test_detect_text_language(self):
        detect = util.detect_language("你好")
        self.assertEqual(detect.result.name, 'Chinese')

    def test_translate_to_english(self):
        util.translate_to_english(COMMON_QUESTION_EXAMPLE_CHINESE)
        self.assertEqual(simple_detect(COMMON_QUESTION_EXAMPLE_CHINESE.question), 'English')

    def test_translate_all(self):
        self.assertTrue(util.translate_all(_read()))


if __name__ == '__main__':
    unittest.main()
