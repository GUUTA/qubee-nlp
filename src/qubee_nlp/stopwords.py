"""
Stop words for Afaan Oromoo language.
"""

from typing import List, Set


class StopWords:
    """
    Stop words manager for Afaan Oromoo.

    IMPORTANT:
    - This module assumes words are ALREADY normalized
    - NO diacritic handling
    - NO Unicode normalization
    """

    def __init__(self, include_common: bool = True):
        self.stopwords: Set[str] = self._load_default_stopwords()

        self.categories = {
            "pronouns": {
                "ANI", "ATE", "ISAN", "ISA", "ISI", "ISII", "NU", "NUU",
                "ISIN", "KEENYA", "KEENYAA", "KEE", "KIYYA",
                "SANI", "SAN"
            },
            "conjunctions": {
                "FI", "YOO", "SILAA", "YEROO", "ERGASII",
                "HAA", "TAY", "AKKAS", "AKKANA"
            },
            "prepositions": {
                "IRRA", "IRRAA", "IRRAAN", "IRRAATTI",
                "KEESSAA", "KEESSATTI", "GADII", "GADI",
                "WAAJIN", "FAANAA"
            },
            "auxiliary_verbs": {
                "TAA", "TAUU", "DHA", "DHAUU",
                "JIRA", "JIRUU"
            },
            "demonstratives": {
                "KUN", "SUN", "KANA", "SANA",
                "AKKANA", "AKKAS"
            },
            "question_words": {
                "EENYUU", "MAAL", "EESSAA", "YOO"
            },
            "adverbs": {
                "AMMA", "AMMAA", "ACHII", "ASI",
                "DHUGAA", "DHUGAATTI"
            }
        }

        if include_common:
            for words in self.categories.values():
                self.stopwords.update(words)

    # ---------------- CORE ---------------- #

    def _load_default_stopwords(self) -> Set[str]:
        return {
            "WAA", "WAAEE", "WAAEEN",

            "ANI", "ATE", "ISA", "ISI", "ISAN",

            "FI", "YOO", "SILAA", "ERGASII",

            "IRRA", "KEESSAA", "GADII",

            "TAA", "DHA", "JIRA",

            "AMMA", "AMMAA", "SANA",

            "EENYUU", "MAAL", "EESSAA",

            "KUN", "SUN", "KANA",

            "HAA", "TAY", "NU", "NUU"
        }

    # ---------------- PUBLIC API ---------------- #

    def is_stopword(self, word: str, check_variants: bool = True) -> bool:
        """
        Check if word is a stop word.

        Assumes word is already normalized.
        """
        if not word:
            return False

        w = word.upper()

        if w in self.stopwords:
            return True

        if check_variants:
            for v in self._get_variants(w):
                if v in self.stopwords:
                    return True

        return False

    def _get_variants(self, word: str) -> List[str]:
        variants = []

        suffixes = ("TI", "TII", "N", "NI", "F", "FI", "S", "SI")
        for suf in suffixes:
            if word.endswith(suf) and len(word) > len(suf):
                variants.append(word[:-len(suf)])

        if word.endswith("KEE"):
            variants.append(word[:-3])
        if word.endswith("SAA"):
            variants.append(word[:-3])
        if word.endswith("SA"):
            variants.append(word[:-2])

        return variants

    def remove_stopwords(self, words: List[str], check_variants: bool = True) -> List[str]:
        return [w for w in words if not self.is_stopword(w, check_variants)]

    def filter_by_category(self, words: List[str], categories: List[str] = None) -> List[str]:
        if not categories:
            return words

        cat_words = set()
        for c in categories:
            if c in self.categories:
                cat_words.update(self.categories[c])

        return [w for w in words if w.upper() not in cat_words]

    def add_stopwords(self, words: List[str]):
        for w in words:
            self.stopwords.add(w.upper())

    def remove_stopwords_set(self, words: Set[str]):
        for w in words:
            self.stopwords.discard(w.upper())

    def get_stopwords(self, categories: List[str] = None) -> Set[str]:
        if not categories:
            return set(self.stopwords)

        result = set()
        for c in categories:
            if c in self.categories:
                result.update(self.categories[c])

        return result


# ---------------- Convenience wrappers ---------------- #

_default = StopWords()

def is_stopword(word: str, check_variants: bool = True) -> bool:
    return _default.is_stopword(word, check_variants)

def remove_stopwords(words: List[str], check_variants: bool = True) -> List[str]:
    return _default.remove_stopwords(words, check_variants)

def get_stopwords_list(categories: List[str] = None) -> List[str]:
    return sorted(_default.get_stopwords(categories))
