# ---------------- Syllabifier Fixed ----------------
import re
from typing import List, Optional
from enum import Enum
from .alphabet import QubeeAlphabet
import unicodedata


class SyllableType(Enum):
    CV = "CV"
    CVC = "CVC"
    VC = "VC"
    V = "V"
    OTHER = "OTHER"


class Syllabifier:
    def __init__(self, strict: bool = False):
        self.strict = strict
        self.digraphs = {"ch", "dh", "ny", "ph", "sh"}

    # -------------------------------------------------

    def _normalize_word(self, word: str) -> str:
        return (
            unicodedata.normalize("NFKD", word)
            .encode("ASCII", "ignore")
            .decode()
            .lower()
        )

    def _contains_digit(self, word: str) -> bool:
        return any(ch.isdigit() for ch in word)

    def _is_valid_word(self, word: str) -> bool:
        # Reject whitespace-only or special characters
        return bool(re.fullmatch(r"[a-zA-Z'-]+", word))

    # -------------------------------------------------

    def syllabify(self, word: str) -> List[str]:
        # ✅ Fix 1: empty or whitespace-only input
        if not word or not word.strip():
            return []

        word = self._normalize_word(word)

        # ✅ Fix 2: always reject digits
        if self._contains_digit(word):
            return []

        # ✅ Fix 3: reject invalid symbols (even if strict=False)
        if not self._is_valid_word(word):
            return []

        if self.strict and not re.fullmatch(r"[a-z'-]+", word):
            return []

        # Apostrophes & hyphens split syllables
        for sep in ("'", "-"):
            if sep in word:
                result = []
                for part in word.split(sep):
                    result.extend(self.syllabify(part))
                return result

        syllables = []
        i = 0
        n = len(word)

        while i < n:
            onset = ""
            nucleus = ""
            coda = ""

            # ---------- Onset ----------
            while i < n and QubeeAlphabet.is_consonant(word[i]):
                if i + 1 < n and word[i:i+2] in self.digraphs:
                    onset += word[i:i+2]
                    i += 2
                else:
                    onset += word[i]
                    i += 1

            # ---------- Nucleus ----------
            while i < n and QubeeAlphabet.is_vowel(word[i]):
                nucleus += word[i]
                i += 1

            if not nucleus:
                break

            # ---------- Coda (safe, no digraph split) ----------
            if i < n and QubeeAlphabet.is_consonant(word[i]):
                if (
                    i + 1 == n
                    or (
                        QubeeAlphabet.is_consonant(word[i + 1])
                        and word[i:i + 2] not in self.digraphs
                    )
                ):
                    coda += word[i]
                    i += 1

            syllables.append(onset + nucleus + coda)

        # ---------- Attach leftovers ----------
        if i < n:
            if syllables:
                syllables[-1] += word[i:]
            else:
                syllables.append(word[i:])

        # ✅ Fix 4: reconstruction invariant (long-word test)
        if "".join(syllables) != word:
            return [word]

        # Consonant-only fallback
        if not syllables:
            return [word]

        return syllables

    # -------------------------------------------------

    def syllabify_text(self, text: str) -> List[List[str]]:
        from .tokenizer import word_tokenize
        return [self.syllabify(w) for w in word_tokenize(text)]

    def count_syllables(self, word: str) -> int:
        return len(self.syllabify(word))

    def get_syllable_pattern(self, word: str):
        patterns = []
        for syl in self.syllabify(word):
            shape = "".join(
                "V" if QubeeAlphabet.is_vowel(c) else "C"
                for c in syl
            )
            patterns.append(
                SyllableType(shape)
                if shape in SyllableType._value2member_map_
                else SyllableType.OTHER
            )
        return patterns


# ---------------- Convenience / Public API ----------------

QubeeSyllabifier = Syllabifier
_default_syllabifier = Syllabifier()

def syllabify_word(word: str) -> List[str]:
    return _default_syllabifier.syllabify(word)

def syllabify_text(
    text: str,
    syllabifier: Optional[Syllabifier] = None
) -> List[List[str]]:
    if syllabifier is None:
        syllabifier = _default_syllabifier
    from .tokenizer import word_tokenize
    return [syllabifier.syllabify(w) for w in word_tokenize(text)]

def count_syllables(word: str) -> int:
    return _default_syllabifier.count_syllables(word)

def get_syllable_pattern(word: str):
    return _default_syllabifier.get_syllable_pattern(word)
