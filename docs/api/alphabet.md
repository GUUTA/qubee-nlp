# Alphabet Module

The `alphabet` module provides utilities for working with the Qubee alphabet used for Afaan Oromoo (Oromo language).

## QubeeAlphabet Class

The main class containing alphabet definitions and validation methods.

### Class Attributes

```python
from qubee_nlp.alphabet import QubeeAlphabet

# Vowels: A, E, I, O, U (with optional diacritics)
print(QubeeAlphabet.VOWELS)  # {'A', 'E', 'I', 'O', 'U'}

# Consonants
print(QubeeAlphabet.CONSONANTS)  # {'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z'}

# All letters
print(QubeeAlphabet.LETTERS)  # Union of vowels and consonants

# Diacritics (for tone marking)
print(QubeeAlphabet.DIACRITICS)  # {'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U', 'á': 'A', 'é': 'E', 'í': 'I', 'ó': 'O', 'ú': 'U'}

# Valid characters
print(QubeeAlphabet.VALID_CHARS)  # All allowed characters

# Digraphs (common consonant combinations)
print(QubeeAlphabet.DIGRAPHS)  # {'CH', 'DH', 'NY', 'PH', 'SH'}

# Diphthongs (common vowel combinations)
print(QubeeAlphabet.DIPHTHONGS)  # {'AE', 'AI', 'AO', 'AU', 'EI', 'EO', 'EU', 'OI', 'OU'}