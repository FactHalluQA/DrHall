from typing import List

from pydantic import BaseModel


class BingResponse(BaseModel):
    text: str = ''
    author: str = ''
    sources: str = ''
    sources_text: str = ''
    suggestions: List[str] = []
    messages_left: int = -1
    max_messages: int = -1
    adaptive_text: str = ''
