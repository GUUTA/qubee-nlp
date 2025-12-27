"""
Qubee Alphabet and text validation utilities for Afaan Oromoo (Oromo language).
"""

import re
from typing import List, Tuple, Set, Dict

# ----------------- Qubee Alphabet Class ----------------- #

class QubeeAlphabet:
    """Qubee alphabet constants and validation utilities for Afaan Oromoo."""

    CONSONANTS: Set[str] = {
        'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M',
        'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z'
    }

    VOWELS: Set[str] = {'A', 'E', 'I', 'O', 'U'}

    LETTERS: Set[str] = CONSONANTS.union(VOWELS)

    SPECIAL_CHARS: Set[str] = {"'", "-"}

    DIACRITICS: Dict[str, str] = {
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'
    }

    VALID_CHARS: Set[str] = (
        LETTERS.union({c.lower() for c in LETTERS})
        .union(SPECIAL_CHARS)
        .union(DIACRITICS.keys())
        .union({' ', '\n', '\t', '.', '!', '?', ',', ';', ':', '(', ')', '[', ']', '"'})
    )

    DIGRAPHS: Set[str] = {'CH', 'DH', 'NY', 'PH', 'SH'}

    DIPHTHONGS: Set[str] = {'AA', 'EE', 'II', 'OO', 'UU'}

    CONSONANT_CLUSTERS: Set[str] = {
        'MB', 'ND', 'NG', 'NJ', 'NK', 'NT',
        'MP', 'LB', 'LD', 'LG', 'LM', 'LN', 'LP', 'LT'
    }

    # ----------------- Character Checks ----------------- #

    @classmethod
    def is_consonant(cls, char: str) -> bool:
        return char.upper() in cls.CONSONANTS if char else False

    @classmethod
    def is_vowel(cls, char: str) -> bool:
        return char.upper() in cls.VOWELS if char else False

    @classmethod
    def is_qubee_letter(cls, char: str) -> bool:
        if not char:
            return False
        if char in cls.DIACRITICS:
            return True
        return char.upper() in cls.LETTERS

    @classmethod
    def is_digraph(cls, text: str) -> bool:
        return text.upper() in cls.DIGRAPHS if text and len(text) == 2 else False

    @classmethod
    def normalize_diacritics(cls, text: str) -> str:
        if text is None:
            return text
        return ''.join(cls.DIACRITICS.get(c, c) for c in text)

    @classmethod
    def get_all_letters(cls) -> List[str]:
        return sorted([c.upper() for c in cls.LETTERS])

    @classmethod
    def normalize_qubee(cls, text: str, preserve_case: bool = False) -> str:
        if text is None:
            return text
        normalized = cls.normalize_diacritics(text)
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        if not preserve_case:
            normalized = normalized.upper()
        return normalized


# ----------------- Module-level wrappers ----------------- #

normalize_qubee = QubeeAlphabet.normalize_qubee

def validate_qubee_text(text: str, strict: bool = False) -> Tuple[bool, List[str]]:
    invalid_chars: List[str] = []
    if text is None:
        return True, invalid_chars
    for char in text:
        if char.isspace():
            continue
        if strict:
            if (char not in QubeeAlphabet.SPECIAL_CHARS and
                char not in QubeeAlphabet.DIACRITICS and
                char.upper() not in QubeeAlphabet.LETTERS):
                if char not in invalid_chars:
                    invalid_chars.append(char)
        else:
            if char not in QubeeAlphabet.VALID_CHARS:
                if char not in invalid_chars:
                    invalid_chars.append(char)
    return len(invalid_chars) == 0, invalid_chars


def is_valid_qubee(text: str, strict: bool = False) -> bool:
    ok, _ = validate_qubee_text(text, strict)
    return ok


def is_valid_afaan_oromoo_word(word: str) -> bool:
    if not word:
        return False
    word = QubeeAlphabet.normalize_diacritics(word)
    word_upper = word.upper()
    if not all(c.isalpha() or c in QubeeAlphabet.SPECIAL_CHARS for c in word_upper):
        return False
    if len(word_upper) == 1:
        return True
    if not any(QubeeAlphabet.is_vowel(c) for c in word_upper):
        return False
    for i in range(len(word_upper)-1):
        a, b = word_upper[i], word_upper[i+1]
        if QubeeAlphabet.is_vowel(a) and QubeeAlphabet.is_vowel(b):
            if (a + b) not in QubeeAlphabet.DIPHTHONGS:
                return False
    for i in range(len(word_upper)-2):
        if (QubeeAlphabet.is_consonant(word_upper[i]) and
            QubeeAlphabet.is_consonant(word_upper[i+1]) and
            QubeeAlphabet.is_consonant(word_upper[i+2])):
            tri = word_upper[i:i+3]
            if tri not in QubeeAlphabet.CONSONANT_CLUSTERS.union({'NTR', 'STR'}):
                return False
    return True


def count_consonants(word: str) -> int:
    if not word:
        return 0
    return sum(1 for c in word.upper() if QubeeAlphabet.is_consonant(c))


def count_vowels(word: str) -> int:
    if not word:
        return 0
    return sum(1 for c in word.upper() if QubeeAlphabet.is_vowel(c))


# ----------------- Syllable splitting ----------------- #
def split_into_syllables(word: str) -> List[str]:
    """Split a word into syllables using CV rules, uppercase all letters."""
    if not word or word.strip() == '':
        return []

    word = QubeeAlphabet.normalize_diacritics(word.strip()).upper()
    syllables = []
    i = 0
    n = len(word)

    while i < n:
        syllable = ''

        # Handle initial consonant(s) including digraphs
        if QubeeAlphabet.is_consonant(word[i]):
            if i + 1 < n and word[i:i+2] in QubeeAlphabet.DIGRAPHS:
                syllable += word[i:i+2]
                i += 2
            else:
                syllable += word[i]
                i += 1

        # Handle vowel(s) including diphthongs
        if i < n and QubeeAlphabet.is_vowel(word[i]):
            if i + 1 < n and word[i:i+2] in QubeeAlphabet.DIPHTHONGS:
                syllable += word[i:i+2]
                i += 2
            else:
                syllable += word[i]
                i += 1

        # Attach remaining consonants at end to next syllable
        if syllable and all(QubeeAlphabet.is_consonant(c) for c in syllable) and syllables:
            syllables[-1] += syllable
        elif syllable:
            syllables.append(syllable)

    return syllables


# ----------------- Module exports ----------------- #

__all__ = [
    "QubeeAlphabet",
    "normalize_qubee",
    "validate_qubee_text",
    "is_valid_qubee",
    "is_valid_afaan_oromoo_word",
    "count_consonants",
    "count_vowels",
    "split_into_syllables",
]
