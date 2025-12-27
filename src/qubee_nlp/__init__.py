# qubee_nlp/__init__.py
# Expose main classes and functions for easy import

# Alphabet
from .alphabet import (
    QubeeAlphabet,
    validate_qubee_text,
    is_valid_qubee,
    normalize_qubee,
    is_valid_afaan_oromoo_word,
    count_consonants,
    count_vowels
)


# Tokenizer
from .tokenizer import (
    QubeeTokenizer,
    word_tokenize,
    tokenize_with_positions,
    tokenize_with_context,
    sentence_tokenize
)

# Normalizer
from .normalizer import TextNormalizer, normalize_text, remove_diacritics

# Syllabifier
# Syllabifier
from .syllabifier import (
    Syllabifier,
    QubeeSyllabifier,
    syllabify_word,
    syllabify_text,
    count_syllables,
    get_syllable_pattern
)


# Stemmer
from .stemmer import (
    QubeeStemmer,
    stem_word,
    lemmatize_word,
    get_word_root
)
