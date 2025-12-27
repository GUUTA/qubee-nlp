"""
Advanced text normalization utilities for Afaan Oromoo (Qubee).
Single source of truth for normalization.
"""

import re
import unicodedata
from typing import List
from .alphabet import QubeeAlphabet


class TextNormalizer:
    """Canonical text normalizer for Afaan Oromoo Qubee."""

    def __init__(
        self,
        normalize_case: bool = True,
        preserve_case: bool = False,
        remove_diacritics: bool = False,
        remove_numbers: bool = False,
        remove_punctuation: bool = False,
        remove_special_chars: bool = False,
        standardize_punctuation: bool = True,
        remove_extra_spaces: bool = True,
    ):
        self.normalize_case = normalize_case
        self.preserve_case = preserve_case
        self.remove_diacritics = remove_diacritics
        self.remove_numbers = remove_numbers
        self.remove_punctuation = remove_punctuation
        self.remove_special_chars = remove_special_chars
        self.standardize_punctuation = standardize_punctuation
        self.remove_extra_spaces = remove_extra_spaces

        # Unicode → ASCII punctuation normalization
        self._punct_map = {
            "’": "'",
            "‘": "'",
            "“": '"',
            "”": '"',
            "–": "-",
            "—": "-",
            "…": "...",
        }

        self._multi_space_re = re.compile(r"\s+", re.UNICODE)
        self._zero_width_re = re.compile(r"[\u200b\u200c\u200d]")  # remove zero-width chars

    # ===================== MAIN API ===================== #

    def normalize(self, text: str) -> str:
        if not text:
            return ""

        # 1. Unicode normalization
        t = unicodedata.normalize("NFC", text)

        # 2. Remove zero-width characters
        t = self._zero_width_re.sub(" ", t)

        # 3. Normalize punctuation symbols
        if self.standardize_punctuation:
            for k, v in self._punct_map.items():
                t = t.replace(k, v)

        # 4. Normalize Qubee-specific diacritics
        if hasattr(QubeeAlphabet, "normalize_diacritics"):
            t = QubeeAlphabet.normalize_diacritics(t)

        # 5. Remove combining accents if requested
        if self.remove_diacritics:
            t = self._strip_diacritics(t)

        # 6. Remove numbers
        if self.remove_numbers:
            t = re.sub(r"\d+", "", t)

        # 7. Remove punctuation (except apostrophes)
        if self.remove_punctuation:
            t = re.sub(r"[.,!?;:]", "", t)

        # 8. Remove special chars (replace hyphens with space, keep apostrophes)
        if self.remove_special_chars:
            t = t.replace("-", " ")
            t = re.sub(r"[^\w\s']", "", t)  # keep letters, digits, spaces, apostrophes

        # 9. Case normalization
        if self.normalize_case and not self.preserve_case:
            t = t.upper()

        # 10. Whitespace cleanup
        if self.remove_extra_spaces:
            t = self._multi_space_re.sub(" ", t).strip()

        return t

    # ===================== HELPERS ===================== #

    def _strip_diacritics(self, text: str) -> str:
        """Remove Unicode combining marks safely, except apostrophes."""
        decomposed = unicodedata.normalize("NFD", text)
        return "".join(c for c in decomposed if not unicodedata.combining(c))

    # ===================== WORD / SENTENCE ===================== #

    def normalize_word(self, word: str) -> str:
        return self.normalize(word or "")

    def normalize_sentence(self, sentence: str) -> str:
        return self.normalize(sentence or "")

    def batch_normalize(self, texts: List[str]) -> List[str]:
        return [self.normalize(t) for t in texts]


# ===================== CONVENIENCE ===================== #

_default_normalizer = TextNormalizer()


def normalize_text(
    text: str,
    preserve_case: bool = False,
    remove_punctuation: bool = False,
    remove_special_chars: bool = False,
    remove_numbers: bool = False,
    remove_diacritics: bool = False,
) -> str:
    return TextNormalizer(
        preserve_case=preserve_case,
        remove_punctuation=remove_punctuation,
        remove_special_chars=remove_special_chars,
        remove_numbers=remove_numbers,
        remove_diacritics=remove_diacritics,
    ).normalize(text)


def remove_diacritics(text: str) -> str:
    return _default_normalizer._strip_diacritics(
        unicodedata.normalize("NFC", text)
    )


def normalize_for_search(text: str) -> str:
    return TextNormalizer(
        normalize_case=True,
        remove_diacritics=True,
        remove_punctuation=True,
        remove_extra_spaces=True,
    ).normalize(text)
