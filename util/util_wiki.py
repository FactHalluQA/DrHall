import re
import urllib
from typing import Any

import wikipediaapi
from wikipediaapi import WikipediaPage

import config


def extract_wiki_titles(raw: Any) -> list[str]:
    """
    Extract wiki titles form Bard's answers.
    """
    try:
        possible_urls = re.findall(
            r'(?:https?://)?en\.wikipedia\.org/wiki/[-a-zA-Z0-9àâçéèêëîïôûùüÿñæœäöÄÖÜß()@:%_+.~#?&/=\']+',
            string=str(raw),
            flags=re.I | re.M)
        urls: list[str] = list(set([url.strip() for url in possible_urls if url.strip()]))
        titles = []
        for url in urls:
            title = urllib.parse.unquote(string=url[(url.index('/wiki/') + 6):],
                                         encoding='utf-8',
                                         errors='replace').strip('\'').strip()
            if title not in titles:
                titles.append(title)
        return titles
    except Exception:
        return []


def fetch_wiki_evidence(titles: list[str]) -> list[WikipediaPage]:
    """
    Fetch wiki summary by titles.
    """
    user_agent = config.USER_AGENT
    wiki_wiki = wikipediaapi.Wikipedia(user_agent=user_agent)
    page_ids = []
    page_list = []
    for title in titles:
        page_py = wiki_wiki.page(title=title)
        if page_py.exists() and (page_py.pageid not in page_ids):
            page_ids.append(page_py.pageid)
            page_list.append(page_py)
    return page_list


def merge_wiki_evidence(pages: list[WikipediaPage]) -> str:
    """
    Build wiki evidence by fetched wikipedia pages.
    Parameters
    ----------
    pages 页面

    Returns
    -------
    wiki evidence字符串
    """
    evidence = ''
    for i in range(len(pages)):
        evidence += re.sub(pattern=r" +",
                           repl=r" ",
                           string='{number}. {content}\n'.format(number=i + 1,
                                                                 content=pages[i].summary.replace("\n", " ")))
    return evidence
