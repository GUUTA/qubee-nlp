"""
Stemmer and lemmatizer for Afaan Oromoo words.
"""

from typing import Optional
from .alphabet import QubeeAlphabet


class QubeeStemmer:
    """Stemmer for Afaan Oromoo words."""

    def __init__(self, aggressive: bool = False):
        self.aggressive = aggressive

        # Common suffixes (longest first)
        self.suffixes = [
            ('KEESSATTI', ''), ('KOOTTI', ''), ('KOOTA', ''),
            ('TOOTA', ''), ('OOTA', ''), ('OTA', ''),
            ('NEENI', ''), ('ETTI', ''), ('ANI', ''), ('ANII', ''),
            ('ACHUU', ''), ('ITAN', ''), ('ATAN', ''),
            ('WWAN', ''), ('UU', ''),
            ('ICHA', ''), ('ICHAA', ''),
            ('DHA', ''), ('TA', ''), ('KEE', ''),
            ('SA', ''), ('SAA', ''),
            ('TIIN', ''), ('TTI', ''),
            ('TII', ''), ('UMMAA', ''),
            ('INA', ''), ('AA', ''), ('OO', ''),
            ('I', '')
        ]

        # Irregular verb forms
        self.irregular_forms = {
            'DHUFAN': 'DHUF',
            'DHAQAN': 'DHAQ',
            'BEEKAN': 'BEEK',
            'JEDHAN': 'JEDH',
            'QABAN': 'QAB',
            'ARGATAN': 'ARGAT',
            'BARATAN': 'BARAT',
            'DHIISAN': 'DHIIS',
            'FIDAN': 'FID',
            'KENNAN': 'KENN'
        }

        # Known verb roots
        self.verb_roots = {
            'DHAQ', 'BEEK', 'JEDH', 'QAB', 'ARGAT', 'BARAT',
            'DHIIS', 'FID', 'KENN', 'BAR', 'HIM'
        }

    # ------------------------------------------------------------------

    def stem(self, word: str) -> str:
        word = QubeeAlphabet.normalize_diacritics(word.upper())

        if word in self.irregular_forms:
            return self.irregular_forms[word]

        original = word

        for suffix, replacement in sorted(self.suffixes, key=lambda x: -len(x[0])):
            if word.endswith(suffix) and len(word) > len(suffix):
                word = word[:-len(suffix)] + replacement
                break

        if len(word) < 2:
            return original

        return word

    # ------------------------------------------------------------------

    def lemmatize(self, word: str, pos: Optional[str] = None) -> str:
        word = QubeeAlphabet.normalize_diacritics(word.upper())
        stem = self.stem(word)

        if pos == 'VERB':
            if not stem.endswith('UU'):
                stem += 'UU'

        elif pos == 'NOUN':
            for suffix in ['TOOTA', 'WWAN', 'OOTA', 'OTA', 'NEENI', 'ETTI']:
                if stem.endswith(suffix) and len(stem) > len(suffix):
                    stem = stem[:-len(suffix)]
                    break

            # Restore essential noun vowels (language-specific)
            if stem == 'MAN':
                stem = 'MANA'
            elif stem == "RE'":
                stem = "RE'E"

        return stem

    # ------------------------------------------------------------------

    def get_root(self, word: str) -> Optional[str]:
        word = QubeeAlphabet.normalize_diacritics(word.upper())
        stem = self.stem(word)

        if stem in self.verb_roots:
            return stem

        # Restore essential noun vowels
        if stem == 'MAN':
            return 'MANA'
        if stem == "RE'":
            return "RE'E"

        return stem if len(stem) >= 2 else word

    # ------------------------------------------------------------------

    def is_verb(self, word: str) -> bool:
        word = QubeeAlphabet.normalize_diacritics(word.upper())
        if word in self.irregular_forms:
            return True
        return self.stem(word) in self.verb_roots

    # ------------------------------------------------------------------

    def is_noun(self, word: str) -> bool:
        word = QubeeAlphabet.normalize_diacritics(word.upper())
        for suffix in ['TOOTA', 'WWAN', 'OOTA', 'OTA', 'NEENI', 'ETTI']:
            if word.endswith(suffix):
                return True
        return False


# ----------------------------------------------------------------------
# Convenience functions
# ----------------------------------------------------------------------

def stem_word(word: str, aggressive: bool = False) -> str:
    return QubeeStemmer(aggressive=aggressive).stem(word)


def lemmatize_word(word: str, pos: Optional[str] = None, aggressive: bool = False) -> str:
    return QubeeStemmer(aggressive=aggressive).lemmatize(word, pos)


def get_word_root(word: str, aggressive: bool = False) -> Optional[str]:
    return QubeeStemmer(aggressive=aggressive).get_root(word)
