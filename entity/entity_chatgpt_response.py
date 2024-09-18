import json
from enum import Enum

import pydantic_core
from pydantic import BaseModel


class ChatGPTResponse(BaseModel):
    class Usage(BaseModel):
        prompt_tokens: int = -1
        completion_tokens: int = -1
        total_tokens: int = -1

    class Choice(BaseModel):
        class Message(BaseModel):
            class Role(str, Enum):
                DEFAULT = None
                SYSTEM = 'system'
                USER = 'user'
                ASSISTANT = 'assistant'
                FUNCTION = 'function'

            class FunctionCall(BaseModel):
                name: str = ''
                arguments: str = ''

            role: Role = Role.DEFAULT
            content: str | None = ''
            function_call: FunctionCall = FunctionCall()

            class Config:
                use_enum_values = True

            def __str__(self):
                return json.dumps(obj=self, ensure_ascii=False, default=pydantic_core.to_jsonable_python)

        index: int = -1
        message: Message = Message()
        finish_reason: str = ''

    id: str = ''
    object: str = ''
    created: int = -1
    model: str = ''
    choices: list[Choice] = []
    usage: Usage = Usage()
