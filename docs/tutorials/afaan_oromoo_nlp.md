I'll reformat this content into a proper `index.md` file while keeping all the information:

## **docs/index.md**


# Qubee NLP Documentation

Welcome to Qubee NLP, a comprehensive Natural Language Processing library for Afaan Oromoo (Oromo language) using the Qubee script.

## Overview

Qubee NLP provides tools for processing, analyzing, and understanding Afaan Oromoo text. The library includes:

* **Text Validation**: Validate Qubee script text
* **Tokenization**: Word and sentence tokenization
* **Normalization**: Text cleaning and standardization
* **Stemming**: Morphological analysis and stemming
* **POS Tagging**: Part-of-speech tagging
* **Stopword Removal**: Language-specific stopword lists
* **Syllabification**: Syllable segmentation

## Quick Start

### Installation


```bash
pip install qubee-nlp
```

### Basic Usage

```python
from qubee_nlp import word_tokenize, sentence_tokenize

# Tokenize text
text = "Afaan Oromoo afaan guddaa dha."
tokens = word_tokenize(text)
print(tokens)  # ['AFAAN', 'OROMOO', 'AFAAN', 'GUDDAA', 'DHA']

sentences = sentence_tokenize("Kuni kitaaba dha. Inni bareessaa dha.")
print(sentences)  # ['KUNI KITAABA DHA.', 'INNI BAREESSAA DHA.']
```

## Features

### 1. Text Validation
Validate that text contains only valid Qubee characters:

```python
from qubee_nlp import validate_qubee_text

is_valid, invalid_chars = validate_qubee_text("Afaan Oromoo")
print(is_valid)  # True
```

### 2. Text Normalization
Normalize text to consistent format:

```python
from qubee_nlp import normalize_qubee

text = "  Áfáan   Oromoo  "
normalized = normalize_qubee(text)
print(normalized)  # "AFAAN OROMOO"
```

### 3. Advanced Tokenization
Tokenize with various options:

```python
from qubee_nlp import QubeeTokenizer

tokenizer = QubeeTokenizer(preserve_case=True)
tokens = tokenizer.tokenize("Afaan Oromoo")
print(tokens)  # ['Afaan', 'Oromoo']
```

### 4. Stemming
Stem Afaan Oromoo words:

```python
from qubee_nlp.stemmer import QubeeStemmer

stemmer = QubeeStemmer()
stem = stemmer.stem("barreessuu")
print(stem)  # "bar"
```

### 5. POS Tagging
Tag parts of speech:

```python
from qubee_nlp.pos import POSTagger

tagger = POSTagger()
tokens = ["Oromoon", "Afaan", "Oromootiin", "dubbatu"]
tags = tagger.tag(tokens)
print(tags)  # ['NOUN', 'NOUN', 'ADP', 'VERB']
```

## Alphabet Module

The `alphabet` module provides utilities for working with the Qubee alphabet used for Afaan Oromoo.

### QubeeAlphabet Class

The main class containing alphabet definitions and validation methods.

#### Class Attributes

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
```

#### Class Methods

##### `is_vowel(char: str) -> bool`
Check if a character is a vowel.

```python
QubeeAlphabet.is_vowel('a')   # True
QubeeAlphabet.is_vowel('b')   # False
QubeeAlphabet.is_vowel('á')   # True (diacritic vowel)
QubeeAlphabet.is_vowel('x')   # False
```

##### `is_consonant(char: str) -> bool`
Check if a character is a consonant.

```python
QubeeAlphabet.is_consonant('b')   # True
QubeeAlphabet.is_consonant('a')   # False
QubeeAlphabet.is_consonant('x')   # True
QubeeAlphabet.is_consonant('1')   # False
```

##### `is_qubee_letter(char: str) -> bool`
Check if a character is a valid Qubee letter.

```python
QubeeAlphabet.is_qubee_letter('a')    # True
QubeeAlphabet.is_qubee_letter('á')    # True (diacritic)
QubeeAlphabet.is_qubee_letter('1')    # False
QubeeAlphabet.is_qubee_letter('ñ')    # False (not in Qubee)
QubeeAlphabet.is_qubee_letter('x')    # True
```

##### `normalize_diacritics(text: str) -> str`
Normalize diacritics to their base letters.

```python
QubeeAlphabet.normalize_diacritics("Áfáan Órómóó")
# Returns: "Afaan Oromoo"

QubeeAlphabet.normalize_diacritics("Cáffée íbidda")
# Returns: "Caffee ibidda"
```

##### `get_all_letters() -> List[str]`
Get all Qubee letters in alphabetical order.

```python
letters = QubeeAlphabet.get_all_letters()
print(letters[:5])  # ['A', 'B', 'C', 'D', 'E']
print(len(letters))  # 26
```

### Functions

#### `validate_qubee_text(text: str, strict: bool = False) -> Tuple[bool, List[str]]`
Validate that text contains only valid Qubee characters for Afaan Oromoo.

**Parameters:**
- `text`: The text to validate
- `strict`: If `True`, only allow letters and basic punctuation (apostrophe, hyphen, space)

**Returns:**
- `Tuple[bool, List[str]]`: (is_valid, list_of_invalid_characters)

**Examples:**
```python
from qubee_nlp.alphabet import validate_qubee_text

# Basic validation
is_valid, invalid_chars = validate_qubee_text("Afaan Oromoo")
print(is_valid)        # True
print(invalid_chars)   # []

# Text with invalid characters
is_valid, invalid_chars = validate_qubee_text("Afaan Oromoo 123")
print(is_valid)        # False
print(invalid_chars)   # ['1', '2', '3']

# Text with diacritics
is_valid, invalid_chars = validate_qubee_text("Áfáan Órómóó")
print(is_valid)        # True
print(invalid_chars)   # []

# Strict validation (only letters and basic punctuation)
is_valid, invalid_chars = validate_qubee_text("Afaan Oromoo!", strict=True)
print(is_valid)        # False (exclamation mark not allowed in strict mode)
print(invalid_chars)   # ['!']

# Strict validation with allowed characters
is_valid, invalid_chars = validate_qubee_text("Afaan-Oromoo waa'ee", strict=True)
print(is_valid)        # True (hyphen and apostrophe are allowed)
```

#### `is_valid_qubee(text: str, strict: bool = False) -> bool`
Convenience function to check if text is valid Qubee.

**Parameters:**
- `text`: The text to check
- `strict`: If `True`, use strict validation rules

**Returns:**
- `bool`: `True` if text is valid Qubee

**Examples:**
```python
from qubee_nlp.alphabet import is_valid_qubee

print(is_valid_qubee("Afaan Oromoo"))      # True
print(is_valid_qubee("Hello 123"))         # False
print(is_valid_qubee("Áfáan"))             # True
print(is_valid_qubee("Afaan Oromoo!"))     # True (lenient mode)
print(is_valid_qubee("Afaan Oromoo!", strict=True))  # False
```

#### `normalize_qubee(text: str, preserve_case: bool = False) -> str`
Normalize Qubee text for Afaan Oromoo.

**Parameters:**
- `text`: The text to normalize
- `preserve_case`: If `True`, preserve original case (default: convert to uppercase)

**Returns:**
- `str`: Normalized text

**Normalization steps:**
1. Normalize diacritics to base letters
2. Convert to uppercase (unless `preserve_case=True`)
3. Replace multiple spaces with single space
4. Remove leading/trailing whitespace

**Examples:**
```python
from qubee_nlp.alphabet import normalize_qubee

# Basic normalization
text = "  Áfáan   Oromoo  "
normalized = normalize_qubee(text)
print(normalized)  # "AFAAN OROMOO"

# Preserve case
normalized_preserve = normalize_qubee("Áfáan Oromoo", preserve_case=True)
print(normalized_preserve)  # "Afaan Oromoo"

# With extra whitespace and diacritics
text = "  Cáffée   íbidda   kéeffata  "
normalized = normalize_qubee(text)
print(normalized)  # "CAFFEE IBIDDA KEEFFATA"
```

#### `split_into_syllables(word: str) -> List[str]`
Split an Afaan Oromoo word into syllables based on Oromo phonotactics.

**Parameters:**
- `word`: The word to split

**Returns:**
- `List[str]`: List of syllables

**Syllable patterns in Afaan Oromoo:**
- CV (consonant-vowel): "baa", "dee", "kii"
- CVC (consonant-vowel-consonant): "bar", "qab", "gud"
- V (vowel): "a", "o", "u"
- VC (vowel-consonant): "ab", "id", "ug"

**Examples:**
```python
from qubee_nlp.alphabet import split_into_syllables

# Simple words
syllables = split_into_syllables("Oromoo")
print(syllables)  # ['O', 'ro', 'moo']

syllables = split_into_syllables("Afaan")
print(syllables)  # ['A', 'faan']

# Complex words
syllables = split_into_syllables("barreessuu")
print(syllables)  # ['bar', 'rees', 'suu']

syllables = split_into_syllables("dubbachuu")
print(syllables)  # ['dub', 'bach', 'uu']

syllables = split_into_syllables("guddina")
print(syllables)  # ['gud', 'di', 'na']

# Words with digraphs
syllables = split_into_syllables("chibbuu")
print(syllables)  # ['chib', 'buu']

syllables = split_into_syllables("shamarree")
print(syllables)  # ['sha', 'mar', 'ree']
```

#### `is_valid_afaan_oromoo_word(word: str) -> bool`
Check if a word follows common Afaan Oromoo word structure patterns.

**Parameters:**
- `word`: The word to check

**Returns:**
- `bool`: `True` if word appears to be a valid Afaan Oromoo word

**Validation rules:**
1. Must contain at least one vowel
2. Should not contain invalid character sequences
3. Follows basic Oromo phonotactic constraints

**Examples:**
```python
from qubee_nlp.alphabet import is_valid_afaan_oromoo_word

print(is_valid_afaan_oromoo_word("Oromoo"))     # True
print(is_valid_afaan_oromoo_word("Afaan"))      # True
print(is_valid_afaan_oromoo_word("barreessuu")) # True
print(is_valid_afaan_oromoo_word("123"))        # False (no vowels)
print(is_valid_afaan_oromoo_word("brr"))        # False (no vowels)
print(is_valid_afaan_oromoo_word("qxz"))        # False (invalid sequence)
```

## Complete Examples

### Text Validation Pipeline

```python
from qubee_nlp.alphabet import (
    QubeeAlphabet,
    validate_qubee_text,
    normalize_qubee,
    split_into_syllables,
    is_valid_afaan_oromoo_word
)

def process_afaan_oromoo_text(text):
    """Complete processing pipeline for Afaan Oromoo text."""
    
    print(f"Original text: '{text}'")
    print("-" * 50)
    
    # Step 1: Validate
    is_valid, invalid_chars = validate_qubee_text(text)
    if not is_valid:
        print(f"Error: Invalid characters found: {invalid_chars}")
        return None
    
    print("✓ Text validation passed")
    
    # Step 2: Normalize
    normalized = normalize_qubee(text, preserve_case=True)
    print(f"✓ Normalized text: '{normalized}'")
    
    # Step 3: Split into words
    words = normalized.split()
    print(f"✓ Words: {words}")
    
    # Step 4: Analyze each word
    print("\nWord Analysis:")
    for word in words:
        # Check if valid Afaan Oromoo word
        is_valid_word = is_valid_afaan_oromoo_word(word)
        
        # Split into syllables
        syllables = split_into_syllables(word)
        
        # Count vowels and consonants
        vowels = [c for c in word if QubeeAlphabet.is_vowel(c)]
        consonants = [c for c in word if QubeeAlphabet.is_consonant(c)]
        
        print(f"  '{word}':")
        print(f"    Valid word: {'Yes' if is_valid_word else 'No'}")
        print(f"    Syllables: {syllables}")
        print(f"    Vowels: {len(vowels)} ({', '.join(vowels)})")
        print(f"    Consonants: {len(consonants)} ({', '.join(consonants)})")
    
    return normalized

# Example usage
text = "Afaan Oromoo guddaa dha."
result = process_afaan_oromoo_text(text)
```

### Character Analysis Utility

```python
from qubee_nlp.alphabet import QubeeAlphabet

def analyze_text_characters(text):
    """Analyze character distribution in text."""
    
    # Initialize counters
    char_stats = {
        'total_chars': 0,
        'vowels': 0,
        'consonants': 0,
        'diacritics': 0,
        'other': 0,
        'vowel_list': [],
        'consonant_list': []
    }
    
    for char in text:
        if char.isspace():
            continue
            
        char_stats['total_chars'] += 1
        
        if char in QubeeAlphabet.DIACRITICS:
            char_stats['diacritics'] += 1
        
        if QubeeAlphabet.is_vowel(char):
            char_stats['vowels'] += 1
            if char not in char_stats['vowel_list']:
                char_stats['vowel_list'].append(char)
        
        elif QubeeAlphabet.is_consonant(char):
            char_stats['consonants'] += 1
            if char not in char_stats['consonant_list']:
                char_stats['consonant_list'].append(char)
        
        else:
            char_stats['other'] += 1
    
    # Calculate percentages
    if char_stats['total_chars'] > 0:
        char_stats['vowel_percent'] = (char_stats['vowels'] / char_stats['total_chars']) * 100
        char_stats['consonant_percent'] = (char_stats['consonants'] / char_stats['total_chars']) * 100
        char_stats['diacritic_percent'] = (char_stats['diacritics'] / char_stats['total_chars']) * 100
    
    return char_stats

# Example usage
text = "Áfáan Órómóó afaan guddaa dha."
stats = analyze_text_characters(text)

print(f"Text: {text}")
print(f"Total characters (excluding spaces): {stats['total_chars']}")
print(f"Vowels: {stats['vowels']} ({stats.get('vowel_percent', 0):.1f}%)")
print(f"Consonants: {stats['consonants']} ({stats.get('consonant_percent', 0):.1f}%)")
print(f"Diacritics: {stats['diacritics']} ({stats.get('diacritic_percent', 0):.1f}%)")
print(f"Unique vowels: {sorted(stats['vowel_list'])}")
print(f"Unique consonants: {sorted(stats['consonant_list'])}")
```

### Word Syllabification Tool

```python
from qubee_nlp.alphabet import split_into_syllables

def syllabify_word(word, show_pattern=False):
    """Syllabify a word and show syllable patterns."""
    
    syllables = split_into_syllables(word)
    
    if not show_pattern:
        return syllables
    
    # Show syllable patterns
    patterns = []
    for syllable in syllables:
        pattern = []
        for char in syllable:
            if QubeeAlphabet.is_vowel(char):
                pattern.append('V')
            elif QubeeAlphabet.is_consonant(char):
                pattern.append('C')
            else:
                pattern.append('?')
        patterns.append(''.join(pattern))
    
    return syllables, patterns

# Example usage
words = ["Oromiyaa", "barreessuu", "dubbachuu", "guddina", "qabxii", "jiraachuu"]

print("Syllabification Examples:")
print("-" * 40)
for word in words:
    syllables, patterns = syllabify_word(word, show_pattern=True)
    print(f"{word:15} → {syllables}")
    print(f"{' ':15}   Patterns: {patterns}")
    print()
```

### Text Cleaner with Validation

```python
from qubee_nlp.alphabet import validate_qubee_text, normalize_qubee

class QubeeTextCleaner:
    """Clean and validate Afaan Oromoo text."""
    
    def __init__(self, strict_mode=False, preserve_case=False):
        self.strict_mode = strict_mode
        self.preserve_case = preserve_case
    
    def clean_text(self, text):
        """Clean text by removing invalid characters."""
        
        # First, validate
        is_valid, invalid_chars = validate_qubee_text(text, self.strict_mode)
        
        if not is_valid and invalid_chars:
            # Remove invalid characters
            for char in invalid_chars:
                text = text.replace(char, '')
        
        # Normalize
        cleaned = normalize_qubee(text, self.preserve_case)
        
        return {
            'cleaned_text': cleaned,
            'original': text,
            'was_valid': is_valid,
            'invalid_chars_removed': invalid_chars if not is_valid else []
        }
    
    def batch_clean(self, texts):
        """Clean multiple texts."""
        
        results = []
        for text in texts:
            result = self.clean_text(text)
            results.append(result)
        
        return results

# Example usage
cleaner = QubeeTextCleaner(strict_mode=False, preserve_case=True)

texts = [
    "Afaan Oromoo 123 test!",
    "Áfáan Órómóó gúddáa",
    "Hello world 456",
    "Oromiyaa's biyya guddaa",
]

results = cleaner.batch_clean(texts)

for i, result in enumerate(results):
    print(f"\nText {i+1}:")
    print(f"  Original: '{result['original']}'")
    print(f"  Cleaned: '{result['cleaned_text']}'")
    if result['invalid_chars_removed']:
        print(f"  Removed: {result['invalid_chars_removed']}")
```

## Qubee Alphabet Reference

### Complete Alphabet Set

```python
# Get all letters
from qubee_nlp.alphabet import QubeeAlphabet

all_letters = QubeeAlphabet.get_all_letters()
print("Qubee Alphabet:")
print("Vowels (5):", [l for l in all_letters if QubeeAlphabet.is_vowel(l)])
print("Consonants (21):", [l for l in all_letters if QubeeAlphabet.is_consonant(l)])
```

### Special Characters in Afaan Oromoo

| Character | Name | Usage | Example |
|-----------|------|-------|---------|
| `'` | Apostrophe | Word-internal glottal stop | `waa'ee` (about) |
| `-` | Hyphen | Compound words, prefixes | `afaan-jalqaba` (first language) |
| `Áá Éé Íí Óó Úú` | Diacritics | Tone marking (optional) | `gúddáa` (big) |

### Common Digraphs

| Digraph | Pronunciation | Example |
|---------|---------------|---------|
| `CH` | Like "ch" in "church" | `chibbuu` (milk) |
| `DH` | Voiced "th" as in "this" | `dhaga'uu` (to hear) |
| `NY` | Like "ny" in "canyon" | `nyaata` (food) |
| `SH` | Like "sh" in "ship" | `shamarree` (leopard) |


## Notes and Best Practices

1. **Case Handling**: Most functions treat text as case-insensitive. Use `preserve_case=True` when you need to maintain original casing.

2. **Diacritics**: While diacritics are part of the Qubee standard for tone marking, they are often omitted in modern writing. The `normalize_diacritics()` function handles both with and without diacritics.

3. **Validation Modes**:
   - **Lenient (default)**: Allows common punctuation marks
   - **Strict**: Only allows letters, apostrophe, hyphen, and space

4. **Performance**: For large texts, consider:
   - Validating once at the beginning
   - Normalizing before multiple operations
   - Using batch processing when possible

5. **Error Handling**: Always check validation results before proceeding with text processing. Invalid characters can cause unexpected behavior.

## API Reference

### Main Modules

- - **Alphabet Module** - Qubee alphabet and validation ([Full Documentation](./api/alphabet.md))
- **Tokenizer Module** - Word and sentence tokenization ([Full Documentation](./api/tokenizer.md))
- **Stemmer Module** - Morphological analysis and stemming ([Full Documentation](./api/stemmer.md))
- **Normalizer Module** - Advanced text normalization
- **POS Module** - Part-of-speech tagging
- **Stopwords Module** - Language-specific stopword lists

## Tutorials

- [Getting Started](./tutorials/getting_started.md) - First steps with Qubee NLP
- [Afaan Oromoo NLP](./tutorials/afaan_oromoo_nlp.md) - Language-specific processing

## Examples

Check the [examples directory](https://github.com/GUUTA/qubee-nlp/tree/main/examples) for complete usage examples:

- [Basic Usage](https://github.com/GUUTA/qubee-nlp/blob/main/examples/basic_usage.py)
- [Tokenization](https://github.com/GUUTA/qubee-nlp/blob/main/examples/tokenization_example.py)
- [Stemming](https://github.com/GUUTA/qubee-nlp/blob/main/examples/stemming_example.py)
- [Advanced Features](https://github.com/GUUTA/qubee-nlp/blob/main/examples/advanced_features.py)

## Contributing

We welcome contributions! Please see our [GitHub repository](https://github.com/GUUTA/qubee-nlp) for contribution guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/GUUTA/qubee-nlp/blob/main/LICENSE) file for details.


This `index.md` file now serves as the main documentation page for Qubee NLP, providing:
- Overview and quick start guide
- Complete alphabet module documentation
- Practical examples
- API reference with links to detailed documentation
- Information about the project and how to contribute

The file maintains all the original content from the alphabet documentation while structuring it as a proper index page with navigation to other parts of the documentation.
## Citation

If you use Qubee NLP in your research, please cite:

```bibtex
@software{qubee_nlp,
  title = {Qubee NLP: Natural Language Processing for Afaan Oromoo},
  author = {Guta Tesema Tufa, Team of Qubee-NLP},
  year = {2025},
  url = {https://github.com/GUUTA/qubee-nlp}
}
