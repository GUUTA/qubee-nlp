# Alphabet Module

The `alphabet` module provides utilities for working with the Qubee alphabet used for Afaan Oromoo (Oromo language).

## QubeeAlphabet Class

The main class containing alphabet definitions and validation methods.



# Qubee Alagaa (Foreign Digraphs)

In Afaan Oromoo (Qubee), Qubee Alagaa refers to foreign digraphs that are not native to the standard Oromo alphabet but may appear in loanwords, names, or technical terms.

The qubee-nlp library explicitly models these digraphs to support:

#### Robust text validation

#### Linguistically aware preprocessing

#### Research-grade NLP pipelines

### Class Attributes

```python
# import this and use it
from qubee_nlp.alphabet import QubeeAlphabet

# Vowels: A, E, I, O, U (without order)
print(QubeeAlphabet.VOWELS)   #{'I', 'E', 'A', 'O', 'U'}

#Qubee dubbachiftuu Tarbibaa kan eegan
print(sorted(QubeeAlphabet.VOWELS)) # {'A', 'E', 'I', 'O', 'U'}

# Consonants without order of the letters, Qubee Dubbifamaa Tartibaa qubee osoo hin eegin.
print(QubeeAlphabet.CONSONANTS)  {'W', 'L', 'K', 'Q', 'V', 'J', 'T', 'Y', 'Z', 'X', 'H', 'M', 'F', 'P', 'R', 'D', 'G', 'B', 'C', 'N', 'S'}

#Consonants with order of the letters, Tartibaa qubee eege.

print(sorted(QubeeAlphabet.CONSINATNTS)) # {'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z'}

# All letters
print(QubeeAlphabet.LETTERS)  # Union of vowels and consonants

#Sorted , Tartibaan
print(sorted(QubeeAlphabet.LETTERS))
#['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
# Diacritics (for tone marking)
print(QubeeAlphabet.DIACRITICS)  # {'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U', 'á': 'A', 'é': 'E', 'í': 'I', 'ó': 'O', 'ú': 'U'}

# Valid characters
print(sorted(QubeeAlphabet.VALID_CHARS)) # All allowed characters ['\t', '\n', ' ', '!', '"', "'", '(', ')', ',', '-', '.', ':', ';', '?', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', ']', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'Á', 'É', 'Í', 'Ó', 'Ú', 'á', 'é', 'í', 'ó', 'ú']

# Digraphs (common consonant combinations), Qubee dachaa 5 kan Afaan oromoo keessatti beekamnii
print(QubeeAlphabet.DIGRAPHS)  # {'CH', 'DH', 'NY', 'PH', 'SH'}

# Diphthongs (common vowel combinations), Qubee dubbachiiftuun yeroo dheeratan
print(QubeeAlphabet.DIPHTHONGS)  # {'AA', 'UU', 'II', 'OO', 'EE'}

#Qubee alagaa 

print(QubeeAlphabet.QUBEE_ALAGAA)  #{'TS', 'ZH'}