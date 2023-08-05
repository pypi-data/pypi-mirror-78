from typing import List
from functools import reduce
from pathlib import Path
import sh

BASE_DIR = Path.home() / ".donno"
REPO = BASE_DIR / "repo"
MD_FILES = list(REPO.glob('*.md'))

def filter_word(file_list: List[str], word: str) -> List[str]:
    if len(file_list) == 0: return []
    return sh.grep('-i', '-l', word, file_list).stdout.decode(
            'UTF-8').strip().split('\n')

def simple_search(word_list: List[str]) -> List[str]:
    return reduce(filter_word, word_list, MD_FILES)

def note_list(file_list: List[str]) -> str:
    return file_list

