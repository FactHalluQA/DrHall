import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

API_KEY = ''
API_KEY_FILE = ROOT_DIR + '\\keys\\chatgpt_api_key'
API_KEY_TEST_FILE = ROOT_DIR + '\\keys\\chatgpt_test_keys'

INPUT_PATH = ROOT_DIR + '\\data\\data.xlsx'
OUTPUT_PATH = ROOT_DIR + '\\data\\output_{mode}_{time}.xlsx'

# 1 - gpt-3.5-turbo
# 2 - text-davinci-002
# 3 - text-davinci-003
GPT_MODEL = 3

BING_COOKIES = ROOT_DIR + '\\keys\\cookies.json'

BARD__Secure_1PSID = ''
BARD__Secure_1PSIDTS = ''
BARD_COOKIE_1 = ROOT_DIR + '\\keys\\BARD__Secure-1PSID'
BARD_COOKIE_2 = ROOT_DIR + '\\keys\\BARD__Secure-1PSIDTS'

SYMBOL_WIKI_FAIL = 'Wiki查找失败！'
SYMBOL_GOOGLE_TRANSLATION_FAIL = 'Google翻译出错！'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 ' \
             'Safari/537.36'

SYMBOL_AI = 'Helpful AI'
SYMBOL_HUMAN = 'Human'

PERSONALITY = 'The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, ' \
              'and very friendly. The assistant is deeply interested in helping people.'

TR_INPUT_PATH = ROOT_DIR + '\\data\\tr_data.xlsx'
TR_OUTPUT_PATH = ROOT_DIR + '\\data\\tr_output_{time}.xlsx'
