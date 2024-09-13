import openai
from loguru import logger

import config
from entity import ChatGPTLegacyResponse, ChatGPTResponse, Models


def get_models() -> Models:
    openai.api_key = __read_key()
    model_list = openai.Model.list()
    return Models.model_validate(model_list)


def chat_with_chatgpt(prompt: str | list[ChatGPTResponse.Choice.Message], api_key: str = '') \
        -> ChatGPTResponse.Choice.Message:
    if api_key:
        openai.api_key = api_key
    else:
        openai.api_key = __read_key()

    if isinstance(prompt, str):
        messages = [{"role": "user", "content": f"{prompt}"}]
    else:
        messages = [message.model_dump() for message in prompt]
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=2048,
        temperature=0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return ChatGPTResponse.model_validate(chat_completion).choices[0].message


def chat_with_chatgpt_legacy(prompt: str, api_key: str = '', model: str = 'text-davinci-003') -> str:
    if api_key:
        openai.api_key = api_key
    else:
        openai.api_key = __read_key()

    completion = openai.Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=1024,
        temperature=0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return ChatGPTLegacyResponse.model_validate(completion).choices[0].text.strip()


def verify_chatgpt_api_keys():
    unavailable_api_keys = []
    available_api_keys = []
    fail = 0
    with open(config.API_KEY_TEST_FILE) as f:
        api_list = [line.strip() for line in f.readlines()]
        for api in api_list:
            try:
                answer: str = \
                    chat_with_chatgpt(
                        "Where did Galileo conduct experiments on the fall of two small balls of  different masses?",
                        api_key=api)[0].strip()
                print(answer)
            except openai.error.RateLimitError:
                unavailable_api_keys.append(api)
                fail = fail + 1
                print(r"Fail times: " + str(fail))
            except Exception as e:
                print(f"Failed to chat with ChatGPT! | Exception: {e}")
            else:
                available_api_keys.append(api)

        if available_api_keys:
            print(r"Available API keys: " + str(available_api_keys))
            print(r"Unavailable API keys: " + str(unavailable_api_keys))
        else:
            print(r"All API keys are unavailable!")


def __read_key() -> str:
    """"
    Read default api key
    """
    if not config.API_KEY:
        with open(config.API_KEY_FILE) as f:
            config.API_KEY = f.readline()
            if not config.API_KEY:
                logger.error(r"Please provide valid ChatGPT api keys!")
    return config.API_KEY
