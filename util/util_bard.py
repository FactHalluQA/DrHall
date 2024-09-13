from Bard import Chatbot

import config
from entity import BardResponse


def chat_with_bard(prompt: str) -> BardResponse:
    chatbot = Chatbot(*__read_cookies__())
    answer_raw = chatbot.ask(prompt)
    return BardResponse.model_validate(answer_raw)


def __read_cookies__() -> tuple[str, str]:
    """
    Read two cookies from cache or file
    """
    secure_1_psid: str
    if config.BARD__Secure_1PSID:
        secure_1_psid = config.BARD__Secure_1PSID
    else:
        with open(config.BARD_COOKIE_1) as f:
            secure_1_psid = f.readline()
            config.BARD__Secure_1PSID = secure_1_psid

    secure_1_psidts: str
    if config.BARD__Secure_1PSIDTS:
        secure_1_psidts = config.BARD__Secure_1PSIDTS
    else:
        with open(config.BARD_COOKIE_2) as f:
            secure_1_psidts = f.readline()
            config.BARD__Secure_1PSIDTS = secure_1_psidts
    return secure_1_psid, secure_1_psidts
