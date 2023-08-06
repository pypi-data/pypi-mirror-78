import unicodedata
from typing import List

def is_whitespace(char: str):
    """Checks whether `char` is a whitespace character."""
    if char == " " or char == "\t" or char == "\n" or char == "\r":
        return True
    cat = unicodedata.category(char)
    if cat == "Zs":
        return True
    return False


def get_char_to_word_map(text: str) -> List[int]:
    words = []
    char_to_word_idx = []
    prev_is_whitespace = True

    for char in text:
        if is_whitespace(char):
            prev_is_whitespace = True
            char_to_word_idx.append(len(words))

        else:
            if prev_is_whitespace:
                words.append(char)
            else:
                words[-1] += char
            prev_is_whitespace = False
            char_to_word_idx.append(len(words) - 1)
    return char_to_word_idx
