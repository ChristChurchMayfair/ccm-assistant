import re
from typing import Dict

import requests
from requests import Response

import config
import secrets


def process_html_passage(raw_passage_html: str) -> str:
    # Remove all double spaces
    passage_html: str = re.sub(r" +", " ", raw_passage_html)

    # Put all verse numbers in square brackets
    passage_html = re.sub(r"<sup(.*?)>(.*?)</sup>", r"[\2] ", passage_html)

    # Remove section headings
    passage_html = re.sub(r"<h(.)(.*?)>(.*?)</h\1>", "", passage_html)

    # Remove all remaining html tags
    passage_html = re.sub(r"<(.*?)>", "", passage_html)

    # Remove all double spaces again
    passage_html = re.sub(r" +", " ", passage_html)
    return passage_html


def get_bible_text(book: str, start_chapter: str, start_verse: str, end_chapter: str, end_verse: str,
                   with_verse_numbers: bool = True) -> str:
    payload: Dict[str, str] = {"q": f"{book}+{start_chapter}:{start_verse}-{end_chapter}:{end_verse}"}
    try:
        response: Response = requests.get(config.BIBLE_API_URL, params=payload, auth=(secrets.BIBLE_API_KEY, "X"))
        passage_html: str = response.json()["response"]["search"]["result"]["passages"][0]["text"]
        processed_passage: str = process_html_passage(passage_html)
        if not with_verse_numbers:
            # Remove section headings
            processed_passage = re.sub(r"( )*\[(.*?)\]( )*", "", processed_passage)
        return processed_passage
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching Bible passage text: {e}")


def remove_square_bracketed_verse_numbers(raw_s: str) -> str:
    s: str = re.sub(r"( )*\[(.*?)\]( )*", "", raw_s)
    s = re.sub(r"\.\b", ". ", s)
    return s
