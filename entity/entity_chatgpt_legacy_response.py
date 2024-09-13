from typing import Any

from pydantic import BaseModel


class ChatGPTLegacyResponse(BaseModel):
    class Usage(BaseModel):
        prompt_tokens: int = -1
        completion_tokens: int = -1
        total_tokens: int = -1

    class Choice(BaseModel):
        text: str = ''
        index: int = -1
        logprobs: Any = None
        finish_reason: str = ''

    id: str = ''
    object: str = ''
    created: int = -1
    model: str = ''
    choices: list[Choice]
    usage: Usage = Usage()
