import asyncio
import json

from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle

import config
from entity import BingResponse


def chat_with_bing(prompt: str) -> BingResponse:
    chatbot: Chatbot = asyncio.run(Chatbot.create(cookies=__read_cookies__()))
    answer_raw = asyncio.run(chatbot.ask(
        prompt=prompt,
        conversation_style=ConversationStyle.precise,
        simplify_response=True
    ))
    return BingResponse.model_validate(answer_raw)


def __read_cookies__() -> list[dict]:
    with open(config.BING_COOKIES, encoding="utf-8") as f:
        return json.loads(f.read())
