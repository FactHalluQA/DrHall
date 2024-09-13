from typing import Any

from pydantic import BaseModel


class BardResponse(BaseModel):
    class Choice(BaseModel):
        id: str = ''
        content: list[str] = []

    content: str = ''
    conversation_id: str = ''
    response_id: str = ''
    factualityQueries: Any = None
    textQuery: str | list = ''
    choices: list[Choice] = []
    images: list = []

    def extract_contents(self) -> list[str]:
        contents = [self.content]
        for choice in self.choices:
            contents.extend(choice.content)
        return list(set(contents))
