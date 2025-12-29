# Advanced Features and Integration Examples for Qubee NLP

This document demonstrates advanced usage patterns, integration capabilities, and extension points of the Qubee NLP library for Afaan Oromoo text processing.

## Table of Contents
- [Stopword Removal and Text Cleaning](#stopword-removal-and-text-cleaning)
- [Part-of-Speech Tagging](#part-of-speech-tagging)
- [Advanced Text Normalization](#advanced-text-normalization)
- [Complete Text Analysis Pipeline](#complete-text-analysis-pipeline)
- [Custom Extensions](#custom-extensions)

## Import Structure

```python
from qubee_nlp import (
    QubeeTokenizer,
    QubeeAlphabet,
    validate_qubee_text,
    normalize_qubee,
    split_into_syllables
)
from qubee_nlp.stopwords import get_stopwords, remove_stopwords
from qubee_nlp.pos import POSTagger, get_afaan_oromoo_tags
from qubee_nlp.normalizer import AdvancedNormalizer
Stopword Removal and Text Cleaning
Features Demonstrated
Retrieval of Afaan Oromoo stopwords

Stopword removal from text

Multi-sentence processing

Example Output
text
=== Stopword Removal ===

Number of stopwords: 150
First 10 stopwords: ['ani', 'asi', 'atu', 'isa', 'isaan', 'isi', 'isin', 'isiin', 'inni', 'isheen']

Original: Afaan Oromoo afaan guddaa Oromiyaati.
Cleaned: Afaan Oromoo afaan guddaa Oromiyaati.

Original: Kuni kitaaba bareessuu dha.
Cleaned: Kuni kitaaba bareessuu.

Original: Ani Oromiyaa keessa jiraadha.
Cleaned: Oromiyaa keessa.
Key Functions
get_stopwords(language='oromo'): Returns a set of stopwords

remove_stopwords(text, language='oromo'): Removes stopwords from text

Part-of-Speech Tagging
Features Demonstrated
Tokenization with QubeeTokenizer

POS tagging with POSTagger

Tag mapping with get_afaan_oromoo_tags()

Example Output
text
=== Part-of-Speech Tagging ===

Sentence: Oromoon Afaan Oromootiin dubbatu.
Tokens and POS tags:
  Oromoon          -> N      (Noun)
  Afaan            -> N      (Noun)
  Oromootiin       -> N      (Noun)
  dubbatu          -> V      (Verb)
Key Classes
POSTagger(): Part-of-speech tagger for Afaan Oromoo

QubeeTokenizer(): Tokenizer for Qubee script

Advanced Text Normalization
Features Demonstrated
Case normalization

Diacritic handling

Extra whitespace removal

Apostrophe and hyphen normalization

Example Output
text
=== Advanced Normalization ===

Original: '  Áfáan   OROMOO    gúddáa   dha.  '
Normalized: 'Afaan Oromoo guddaa dha.'

Original: "Oromiyaa's biyya' guddaa' dha."
Normalized: 'Oromiyaa biyya guddaa dha.'

Original: 'Afaan-Oromoo afaan jalqaba-dha.'
Normalized: 'Afaan Oromoo afaan jalqaba dha.'
Key Class
AdvancedNormalizer(): Comprehensive text normalizer

Complete Text Analysis Pipeline
Seven-Step Processing Pipeline
Text Validation - Checks for valid Qubee characters

Normalization - Standardizes text format

Tokenization - Splits text into tokens

Stopword Removal - Filters common words

POS Tagging - Identifies grammatical categories

Frequency Analysis - Calculates word frequencies

Syllable Analysis - Breaks words into syllables

Example Output
text
=== Complete Text Analysis Pipeline ===

Original Text:
Afaan Oromoo afaan Kushitikii kan dubbatamu Oromiyaa fi naannawa ishee keessatti dha.
...

1. Validation:
   Valid: True
   Invalid characters: []

2. Normalization:
   Normalized text: Afaan Oromoo afaan Kushitikii kan dubbatamu...

3. Tokenization:
   Number of tokens: 25
   First 10 tokens: ['Afaan', 'Oromoo', 'afaan', 'Kushitikii', ...]

4. Stopword Removal:
   Tokens after stopword removal: 18
   Removed 7 stopwords

5. POS Tagging (first 10):
   Afaan           -> N
   Oromoo          -> N
   afaan           -> N
   ...

6. Frequency Analysis:
   Most common words:
   Afaan          : 3
   Oromoo         : 2
   afaan          : 2
   ...

7. Syllable Analysis:
   Afaan           -> ['A', 'faa', 'n']
   Oromoo          -> ['O', 'ro', 'moo']
   ...
Custom Extensions
Creating Custom Filters
python
class CustomTokenFilter:
    def __init__(self, min_length=3):
        self.min_length = min_length
        
    def filter(self, tokens):
        return [
            token for token in tokens 
            if len(token) >= self.min_length 
            and not token.isdigit()
        ]
Dialect Normalization
python
class DialectNormalizer:
    """Normalize dialectal variations."""
    
    DIALECT_MAP = {
        'waan': 'wanti',    # Some dialect variations
        'isan': 'isaan',
        'inni': 'inniinu',
    }
    
    def normalize(self, text):
        normalized = text
        for dialect, standard in self.DIALECT_MAP.items():
            normalized = normalized.replace(dialect, standard)
        return normalized
Example Output
text
=== Custom Extensions ===

Original tokens: ['Waan', 'isan', 'jedhan', 'inni', 'sirrii', 'dha']
Filtered tokens (min length 4): ['Waan', 'isan', 'jedhan', 'inni', 'sirrii']

Original text: Waan isan jedhan inni sirrii dha.
Dialect-normalized: Wanti isaan jedhan inniinu sirrii dha.
Usage Examples
Running All Demonstrations
python
if __name__ == "__main__":
    demonstrate_stopword_removal()
    demonstrate_pos_tagging()
    demonstrate_advanced_normalization()
    demonstrate_text_analysis_pipeline()
    demonstrate_custom_extensions()