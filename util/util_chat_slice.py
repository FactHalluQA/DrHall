from loguru import logger

import config
import util
from entity import AIModel, ExperimentException


class ChatSlice(object):
    def __init__(self, prompt: str, model: AIModel = AIModel.ChatGPT):
        self._model: AIModel = model

        self._prompt: str = prompt
        self._answer: str = self.__answer()

    @property
    def prompt(self) -> str:
        return self._prompt

    @prompt.setter
    def prompt(self, new_prompt: str) -> None:
        self._prompt = new_prompt
        self._answer: str = self.__answer()

    @property
    def model(self) -> AIModel:
        return self._model

    @model.setter
    def model(self, model: AIModel) -> None:
        self._model = model

    @property
    def answer(self) -> str:
        return self._answer

    def __answer(self) -> str:
        if self._model == AIModel.ChatGPT:
            return util.chat_with_chatgpt(prompt=self.prompt).content
        elif self._model == AIModel.ChatGPTLegacy:
            return util.chat_with_chatgpt_legacy(prompt=self.prompt)
        elif self._model == AIModel.Bard:
            return util.chat_with_bard(prompt=self.prompt).content
        else:
            raise ExperimentException("Unknown model!")


def create_chat_slice(prompt: str) -> ChatSlice:
    if config.GPT_MODEL == 1:  # gpt-3.5-turbo
        return ChatSlice(prompt=prompt, model=AIModel.ChatGPT)
    elif config.GPT_MODEL == 2:  # text-davinci-002
        logger.warning("Do not use this model!", DeprecationWarning)
    elif config.GPT_MODEL == 3:  # text-davinci-003
        return ChatSlice(prompt=prompt, model=AIModel.ChatGPTLegacy)
    else:
        logger.error("Unknown model!")
