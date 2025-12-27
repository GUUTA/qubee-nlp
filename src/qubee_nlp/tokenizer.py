import re
import unicodedata
from typing import List, Dict, Any

class QubeeTokenizer:
    """
    Tokenizer for Afaan Oromoo text written in Qubee.

    Features:
    - Preserves valid Afaan Oromoo orthography (e.g., 'Oromoo' stays 'Oromoo')
    - Optional strict mode (disallow digits)
    - Optional case preservation
    """

    # Match words with letters, apostrophes, and hyphens
    _word_pattern = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+(?:['-][A-Za-zÀ-ÖØ-öø-ÿ]+)*")

    # Common abbreviations to protect during sentence splitting
    _abbreviations = {"DR.", "PROF.", "MR.", "MRS.", "MS."}

    def __init__(self, preserve_case: bool = False, strict: bool = False):
        self.preserve_case = preserve_case
        self.strict = strict

    # -----------------------------
    # Helpers
    # -----------------------------
    def _strip_diacritics(self, text: str) -> str:
        """
        Remove diacritics while preserving valid Oromo letters and double vowels.
        """
        text = unicodedata.normalize("NFD", text)
        # Keep letters that are A-Z, a-z, Oromo vowels, or non-combining characters
        return "".join(
            c for c in text
            if unicodedata.category(c) != "Mn" or c in "aeiouAEIOU"
        )

    def _normalize_token(self, token: str) -> str:
        """
        Normalize token: strip diacritics but preserve Oromo spelling.
        """
        token = self._strip_diacritics(token)
        return token if self.preserve_case else token.upper()

    def _validate_strict_text(self, text: str):
        if re.search(r"\d", text):
            raise ValueError("Digits are not allowed in strict mode")

    def _validate_strict_token(self, token: str):
        if re.search(r"\d", token):
            raise ValueError(f"Invalid token in strict mode: {token}")

    # -----------------------------
    # Tokenization
    # -----------------------------
    def tokenize(self, text: str) -> List[str]:
        if not isinstance(text, str):
            raise ValueError("Input must be a string")
        if not text.strip():
            return []

        if self.strict:
            self._validate_strict_text(text)

        tokens = self._word_pattern.findall(text)
        if self.strict and not tokens:
            raise ValueError("No valid tokens found")

        normalized = []
        for t in tokens:
            if self.strict:
                self._validate_strict_token(t)
            normalized.append(self._normalize_token(t))

        return normalized

    def tokenize_with_positions(self, text: str) -> List[Dict[str, Any]]:
        if not isinstance(text, str):
            raise ValueError("Input must be a string")
        if self.strict:
            self._validate_strict_text(text)

        results = []
        for m in self._word_pattern.finditer(text):
            token = m.group()
            if self.strict:
                self._validate_strict_token(token)
            results.append({
                "token": self._normalize_token(token),
                "start": m.start(),
                "end": m.end(),
                "length": m.end() - m.start()
            })

        return results

    def tokenize_with_context(self, text: str, context_chars: int = 2):
        tokens = self.tokenize_with_positions(text)
        for t in tokens:
            s, e = t["start"], t["end"]
            t["left_context"] = text[max(0, s - context_chars):s]
            t["right_context"] = text[e:e + context_chars]
        return tokens

    # -----------------------------
    # Sentence Tokenization
    # -----------------------------
    def sentence_tokenize(self, text: str) -> List[str]:
        if not isinstance(text, str):
            raise ValueError("Input must be a string")
        if not text.strip():
            return []

        if self.strict:
            self._validate_strict_text(text)

        processed = self._strip_diacritics(text)
        processed = processed if self.preserve_case else processed.upper()

        protected = processed
        for abbr in self._abbreviations:
            protected = protected.replace(
                abbr if self.preserve_case else abbr.upper(),
                abbr.replace(".", "<DOT>")
            )

        parts = re.split(r"(?<=[.!?])\s+", protected)

        sentences = []
        for p in parts:
            p = p.replace("<DOT>", ".").strip()
            if p:
                sentences.append(p)

        return sentences

# -----------------------------
# Convenience Functions
# -----------------------------
def word_tokenize(text: str, preserve_case=False, strict=False):
    return QubeeTokenizer(preserve_case, strict).tokenize(text)

def sentence_tokenize(text: str, preserve_case=False, strict=False):
    return QubeeTokenizer(preserve_case, strict).sentence_tokenize(text)

def tokenize_with_positions(text: str, preserve_case=False, strict=False):
    return QubeeTokenizer(preserve_case, strict).tokenize_with_positions(text)

def tokenize_with_context(text: str, context_chars=2, preserve_case=False, strict=False):
    return QubeeTokenizer(preserve_case, strict).tokenize_with_context(text, context_chars=context_chars)
