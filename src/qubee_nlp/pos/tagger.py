import re
import string
from typing import List
from .tagsets import VERB_SUFFIXES, NOUN_SUFFIXES, map_to_universal

DEFAULT_TAG = "UNK"
NUM_TAG = "NUM"
PUNC_TAG = "PUNC"

# Lexicon for common words with fixed POS
LEXICON = {
    # adjectives
    "guddaa": "ADJ",
    "xixiqqoo": "ADJ",
    # nouns
    "waa'ee": "NOUN",
    "afaan": "NOUN",
    "biyya": "NOUN",
    # pronouns
    "ani": "PRON",
    "isin": "PRON",
    # add more exceptions as needed
}

# Prepositions (adpositions) in Afaan Oromoo
PREPOSITIONS = {
    "fi", "yookiin", "gara", "jalatti", "bira", "keessa", "alaa", "wajjin", "malee", "waa'ee"
}

class QubeePOSTagger:
    """Rule-based POS tagger for Afaan Oromoo with lexicon overrides."""

    def __init__(self):
        self.model = "rule-based"

    def tag(self, tokens: List[str]) -> List[str]:
        if not tokens:
            return []
        return [self._tag_token(t) for t in tokens]

    def _tag_token(self, token: str) -> str:
        t = token.strip()
        if not t:
            return DEFAULT_TAG

        t_lower = t.lower()

        # 0️⃣ Lexicon overrides
        if t_lower in LEXICON:
            return LEXICON[t_lower]

        # 1️⃣ Numbers (digits or Afaan Oromoo number words)
        afaan_oromoo_numbers = {
            "tokko", "lama", "sadi", "afur", "shan", "jahaa",
            "torba", "saddeet", "sagal", "kudha"
        }
        if t_lower in afaan_oromoo_numbers or re.fullmatch(r"\d+(\.\d+)?", t_lower):
            return NUM_TAG

        # 2️⃣ Punctuation-only (excluding apostrophe)
        if all(c in string.punctuation.replace("'", "") for c in t_lower):
            return PUNC_TAG

        # 3️⃣ Prepositions (Adpositions)
        if t_lower in PREPOSITIONS:
            return "ADP"

        # 4️⃣ Conjunctions
        if t_lower in {"fi", "yookiin"}:
            return "CONJ"

        # 5️⃣ Verb suffixes
        for suffix, tag in VERB_SUFFIXES.items():
            if t_lower.endswith(suffix):
                return map_to_universal(tag)

        # 6️⃣ Noun suffixes
        for suffix, tag in NOUN_SUFFIXES.items():
            if t_lower.endswith(suffix):
                return map_to_universal(tag)

        # 7️⃣ Hyphen or apostrophe heuristic → NOUN
        if re.fullmatch(r"[a-zA-Z'-]+", t_lower):
            if "-" in t_lower or "'" in t_lower:
                return "NOUN"
            # If unknown, default to ADJ for common adjective endings
            if t_lower.endswith(("aa", "oo", "uu")):  # common adjective endings
                return "ADJ"
            return DEFAULT_TAG

        # 8️⃣ Anything else → X
        return "X"


# Optional n-gram taggers (inherit same logic)
class UnigramTagger(QubeePOSTagger): pass
class BigramTagger(QubeePOSTagger): pass
class TrigramTagger(QubeePOSTagger): pass
