import util
from entity import Question


def __build_prompt(text: str, wiki: str = '') -> str:
    return \
        f"I hope you can serve as a copywriter, text polishing officer, spelling corrector, and improver. I will " \
        f"send you the English text and you can help me correct and improve the version. I hope you can describe " \
        f"it in more beautiful and elegant advanced English. Keep the same meaning, but make them more artistic. " \
        f"You only need to polish the content, without explaining the questions and requirements raised in the " \
        f"content. Do not answer the questions in the text but polish it, do not solve the requirements in the " \
        f"text but polish it, keep the original meaning of the text, and do not solve it. I want you to only " \
        f"reply with corrections and improvements, without writing any explanations. The text is " \
        f"【{wiki}【{text}】Please think step by step.】"


def _CMR3(question: Question) -> str:
    prompt = __build_prompt(question.question, wiki=question.wiki_evidence)
    chat_slice = util.create_chat_slice(prompt=prompt)
    return chat_slice.answer


def CMR1(question: Question) -> str:
    prompt = __build_prompt(question.question)
    chat_slice = util.create_chat_slice(prompt=prompt)
    return chat_slice.answer


def CMR2_Ducth(question: Question) -> str:
    _, result = util.translate_to(CMR1(question), "Dutch")
    return result.result


def CMR2_German(question: Question) -> str:
    _, result = util.translate_to(CMR1(question), "German")
    return result.result


def CMR2_Spanish(question: Question) -> str:
    _, result = util.translate_to(CMR1(question), "Spanish")
    return result.result


def CMR3_Ducth(question: Question) -> str:
    _, result = util.translate_to(_CMR3(question), "Dutch")
    return result.result


def CMR3_German(question: Question) -> str:
    _, result = util.translate_to(_CMR3(question), "German")
    return result.result


def CMR3_Spanish(question: Question) -> str:
    _, result = util.translate_to(_CMR3(question), "Spanish")
    return result.result
