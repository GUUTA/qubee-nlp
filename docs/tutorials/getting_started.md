I'll create the `getting_started.md` file for the tutorials section:

## **docs/tutorials/getting_started.md**

```markdown
# Getting Started with Qubee NLP

This tutorial will guide you through installing and using the Qubee NLP library for Afaan Oromoo text processing.

## Prerequisites

Before you begin, make sure you have:

- **Python 3.7 or higher** installed
- **Basic knowledge of Python** programming
- **Familiarity with Afaan Oromoo** (Oromo language) is helpful but not required
- **Text editor or IDE** (VS Code, PyCharm, or any Python IDE)

## Installation

### Method 1: Install from PyPI (Recommended)

```bash
pip install qubee-nlp
```

### Method 2: Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/qubee-nlp.git
cd qubee-nlp

# Install in development mode
pip install -e .

# Install development dependencies (optional)
pip install -e .[dev]
```

### Verify Installation

```python
import qubee_nlp
print(f"Qubee NLP version: {qubee_nlp.__version__}")
```

## Understanding Qubee Script

Qubee is the Latin-based alphabet used for writing Afaan Oromoo. Here are the basics:

```python
from qubee_nlp.alphabet import QubeeAlphabet

# Qubee has 5 vowels
print("Vowels:", QubeeAlphabet.VOWELS)  
# Output: {'A', 'E', 'I', 'O', 'U'}

# And 21 consonants
print("Number of consonants:", len(QubeeAlphabet.CONSONANTS))  
# Output: 21

# Diacritics are sometimes used for tone marking (optional)
print("Diacritic mapping (first 3):", dict(list(QubeeAlphabet.DIACRITICS.items())[:3]))
# Output: {'Á': 'A', 'É': 'E', 'Í': 'I'}
```

### Qubee Alphabet Overview

| Category | Letters | Description |
|----------|---------|-------------|
| Vowels | A, E, I, O, U | Basic vowels (with optional diacritics: á, é, í, ó, ú) |
| Consonants | B, C, D, F, G, H, J, K, L, M, N, P, Q, R, S, T, V, W, X, Y, Z | 21 consonants |
| Digraphs | CH, DH, NY, PH, SH | Common consonant combinations |
| Special | ' (apostrophe), - (hyphen) | Used in words like "waa'ee" (about) |

## Your First Qubee NLP Program

Create a file `first_program.py`:

```python
#!/usr/bin/env python3
"""First program with Qubee NLP."""

from qubee_nlp import word_tokenize, sentence_tokenize

def main():
    # Sample Afaan Oromoo text
    text = "Afaan Oromoo afaan jalqaba Oromiyaati. Waa'ee isaa dubbachuun barbaachisaa dha."
    
    # Tokenize into words
    words = word_tokenize(text)
    print(f"Words: {words}")
    
    # Tokenize into sentences
    sentences = sentence_tokenize(text)
    print(f"\nSentences: {sentences}")
    
    # Basic statistics
    print(f"\nStatistics:")
    print(f"  Text length: {len(text)} characters")
    print(f"  Number of words: {len(words)}")
    print(f"  Number of sentences: {len(sentences)}")
    print(f"  Average words per sentence: {len(words)/len(sentences):.1f}")

if __name__ == "__main__":
    main()
```

Run it:
```bash
python first_program.py
```

**Expected Output:**
```
Words: ['AFAAN', 'OROMOO', 'AFAAN', 'JALQABA', 'OROMIYAATI', 'WAA\'EE', 'ISAA', 'DUBBACHUUN', 'BARBAACHISAA', 'DHA']
Sentences: ['AFAAN OROMOO AFAAN JALQABA OROMIYAATI.', 'WAA\'EE ISAA DUBBACHUUN BARBAACHISAA DHA.']

Statistics:
  Text length: 70 characters
  Number of words: 10
  Number of sentences: 2
  Average words per sentence: 5.0
```

## Core Concepts

### 1. Text Validation

Always validate your text before processing:

```python
from qubee_nlp import validate_qubee_text

# Valid Afaan Oromoo text
text1 = "Afaan Oromoo afaan guddaa dha."
is_valid1, invalid1 = validate_qubee_text(text1)
print(f"Text 1 valid: {is_valid1}, Invalid chars: {invalid1}")
# Output: Text 1 valid: True, Invalid chars: []

# Text with invalid characters
text2 = "Afaan Oromoo 123 test!"
is_valid2, invalid2 = validate_qubee_text(text2)
print(f"Text 2 valid: {is_valid2}, Invalid chars: {invalid2}")
# Output: Text 2 valid: False, Invalid chars: ['1', '2', '3', '!']
```

### 2. Text Normalization

Normalize text to consistent format:

```python
from qubee_nlp import normalize_qubee

# Text with diacritics and extra spaces
text = "  Áfáan   Oromoo  gúddáa   dha.  "
normalized = normalize_qubee(text)
print(f"Normalized: '{normalized}'")
# Output: Normalized: 'AFAAN OROMOO GUDDAA DHA.'

# Preserve case
normalized_preserve = normalize_qubee("Áfáan Oromoo", preserve_case=True)
print(f"Preserved case: '{normalized_preserve}'")
# Output: Preserved case: 'Afaan Oromoo'
```

### 3. Tokenization

Tokenize text into words and sentences:

```python
from qubee_nlp import QubeeTokenizer

# Create tokenizer with options
tokenizer = QubeeTokenizer(
    preserve_case=True,  # Keep original case
    strict=False         # Use lenient validation
)

text = "Afaan Oromoo afaan jalqaba Oromiyaati."
tokens = tokenizer.tokenize(text)
print(f"Tokens: {tokens}")
# Output: Tokens: ['Afaan', 'Oromoo', 'afaan', 'jalqaba', 'Oromiyaati']

sentences = tokenizer.sentence_tokenize(text + " Kunis dubbii dha.")
print(f"Sentences: {sentences}")
# Output: Sentences: ['Afaan Oromoo afaan jalqaba Oromiyaati.', 'Kunis dubbii dha.']
```

### 4. Character Analysis

Analyze text at character level:

```python
from qubee_nlp.alphabet import QubeeAlphabet

def analyze_characters(text):
    """Analyze character distribution in text."""
    vowels = consonants = others = 0
    vowel_list = []
    consonant_list = []
    
    for char in text:
        if char.isspace():
            continue
            
        if QubeeAlphabet.is_vowel(char):
            vowels += 1
            if char.upper() not in vowel_list:
                vowel_list.append(char.upper())
        elif QubeeAlphabet.is_consonant(char):
            consonants += 1
            if char.upper() not in consonant_list:
                consonant_list.append(char.upper())
        else:
            others += 1
    
    total = vowels + consonants + others
    return {
        'vowels': vowels,
        'consonants': consonants,
        'others': others,
        'total': total,
        'vowel_percent': (vowels / total * 100) if total > 0 else 0,
        'consonant_percent': (consonants / total * 100) if total > 0 else 0,
        'vowel_list': sorted(vowel_list),
        'consonant_list': sorted(consonant_list)
    }

text = "Afaan Oromoo"
stats = analyze_characters(text)
print(f"Vowels: {stats['vowels']} ({stats['vowel_percent']:.1f}%)")
print(f"Consonants: {stats['consonants']} ({stats['consonant_percent']:.1f}%)")
print(f"Unique vowels: {stats['vowel_list']}")
print(f"Unique consonants: {stats['consonant_list']}")
```

## Step-by-Step Tutorial

### Step 1: Setting Up Your Project

1. Create a new directory for your project:
```bash
mkdir my_qubee_project
cd my_qubee_project
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

4. Install Qubee NLP:
```bash
pip install qubee-nlp
```

### Step 2: Create a Simple Text Analyzer

Create `analyzer.py`:

```python
#!/usr/bin/env python3
"""Simple Afaan Oromoo text analyzer."""

from qubee_nlp import (
    word_tokenize,
    sentence_tokenize,
    validate_qubee_text,
    normalize_qubee
)
from qubee_nlp.alphabet import QubeeAlphabet

class SimpleTextAnalyzer:
    def __init__(self):
        self.results = {}
    
    def analyze(self, text):
        """Analyze Afaan Oromoo text."""
        
        # Store original text
        self.results['original'] = text
        
        # Validate
        is_valid, invalid_chars = validate_qubee_text(text)
        self.results['is_valid'] = is_valid
        self.results['invalid_chars'] = invalid_chars
        
        if not is_valid:
            return self.results
        
        # Normalize
        normalized = normalize_qubee(text, preserve_case=True)
        self.results['normalized'] = normalized
        
        # Tokenize
        words = word_tokenize(normalized, preserve_case=True)
        sentences = sentence_tokenize(normalized, preserve_case=True)
        
        self.results['words'] = words
        self.results['sentences'] = sentences
        self.results['word_count'] = len(words)
        self.results['sentence_count'] = len(sentences)
        self.results['avg_words_per_sentence'] = len(words) / len(sentences) if sentences else 0
        
        # Character analysis
        self._analyze_characters(text)
        
        return self.results
    
    def _analyze_characters(self, text):
        """Analyze character distribution."""
        vowels = consonants = 0
        
        for char in text:
            if char.isspace():
                continue
            if QubeeAlphabet.is_vowel(char):
                vowels += 1
            elif QubeeAlphabet.is_consonant(char):
                consonants += 1
        
        total_chars = vowels + consonants
        self.results['character_stats'] = {
            'vowels': vowels,
            'consonants': consonants,
            'total': total_chars,
            'vowel_percent': (vowels / total_chars * 100) if total_chars > 0 else 0,
            'consonant_percent': (consonants / total_chars * 100) if total_chars > 0 else 0
        }
    
    def print_report(self):
        """Print analysis report."""
        print("=" * 60)
        print("AFAN OROMOO TEXT ANALYSIS REPORT")
        print("=" * 60)
        
        print(f"\nOriginal Text: {self.results['original'][:50]}..." 
              if len(self.results['original']) > 50 else self.results['original'])
        
        print(f"\nVALIDATION:")
        print(f"  Valid: {'✓ Yes' if self.results['is_valid'] else '✗ No'}")
        if not self.results['is_valid']:
            print(f"  Invalid characters: {self.results['invalid_chars']}")
        
        if self.results['is_valid']:
            print(f"\nNORMALIZED TEXT: {self.results['normalized']}")
            
            print(f"\nTOKENIZATION:")
            print(f"  Words: {self.results['word_count']}")
            print(f"  Sentences: {self.results['sentence_count']}")
            print(f"  Average words/sentence: {self.results['avg_words_per_sentence']:.1f}")
            
            print(f"\nCHARACTER ANALYSIS:")
            stats = self.results['character_stats']
            print(f"  Vowels: {stats['vowels']} ({stats['vowel_percent']:.1f}%)")
            print(f"  Consonants: {stats['consonants']} ({stats['consonant_percent']:.1f}%)")
            print(f"  Total characters: {stats['total']}")
            
            print(f"\nSAMPLE WORDS (first 5):")
            for word in self.results['words'][:5]:
                print(f"  - {word}")

# Example usage
if __name__ == "__main__":
    analyzer = SimpleTextAnalyzer()
    
    sample_texts = [
        "Afaan Oromoo afaan guddaa dha.",
        "Oromiyaan biyya guddaa Afriikaa keessatti argamti.",
        "Qubee sirna barreeffama Afaan Oromoo dha.",
    ]
    
    for i, text in enumerate(sample_texts, 1):
        print(f"\n\n{'='*60}")
        print(f"ANALYSIS {i}")
        print(f"{'='*60}")
        analyzer.analyze(text)
        analyzer.print_report()
```

Run the analyzer:
```bash
python analyzer.py
```

### Step 3: Working with Files

Create `file_processor.py`:

```python
#!/usr/bin/env python3
"""Process Afaan Oromoo text files."""

import os
from pathlib import Path
from qubee_nlp import word_tokenize, sentence_tokenize
from qubee_nlp.alphabet import validate_qubee_text
from collections import Counter

class FileProcessor:
    def __init__(self):
        self.results = {}
    
    def process_file(self, filepath):
        """Process a text file containing Afaan Oromoo text."""
        
        if not os.path.exists(filepath):
            print(f"Error: File not found: {filepath}")
            return None
        
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        
        print(f"\nProcessing file: {filepath}")
        print(f"File size: {len(text):,} characters")
        
        # Validate
        is_valid, invalid_chars = validate_qubee_text(text)
        if not is_valid:
            print(f"Warning: Invalid characters found: {invalid_chars}")
        
        # Tokenize
        words = word_tokenize(text)
        sentences = sentence_tokenize(text)
        
        # Statistics
        word_counts = Counter(words)
        unique_words = set(words)
        
        result = {
            'filepath': filepath,
            'characters': len(text),
            'words': len(words),
            'sentences': len(sentences),
            'unique_words': len(unique_words),
            'is_valid': is_valid,
            'invalid_chars': invalid_chars,
            'most_common_words': word_counts.most_common(10),
            'lexical_diversity': len(unique_words) / len(words) if words else 0
        }
        
        self._print_summary(result)
        return result
    
    def _print_summary(self, result):
        """Print processing summary."""
        print(f"\nSUMMARY:")
        print(f"  Characters: {result['characters']:,}")
        print(f"  Words: {result['words']:,}")
        print(f"  Sentences: {result['sentences']:,}")
        print(f"  Unique words: {result['unique_words']:,}")
        print(f"  Lexical diversity: {result['lexical_diversity']:.3f}")
        print(f"  Valid Qubee: {'✓ Yes' if result['is_valid'] else '✗ No'}")
        
        if result['most_common_words']:
            print(f"\nTOP 10 MOST COMMON WORDS:")
            for word, count in result['most_common_words']:
                percentage = (count / result['words']) * 100
                print(f"  {word:15} {count:5} ({percentage:.1f}%)")
    
    def batch_process(self, directory):
        """Process all text files in a directory."""
        
        directory = Path(directory)
        if not directory.exists() or not directory.is_dir():
            print(f"Error: Directory not found: {directory}")
            return []
        
        results = []
        for filepath in directory.glob('*.txt'):
            result = self.process_file(filepath)
            if result:
                results.append(result)
        
        self._print_batch_summary(results)
        return results
    
    def _print_batch_summary(self, results):
        """Print batch processing summary."""
        if not results:
            return
        
        print(f"\n{'='*60}")
        print(f"BATCH PROCESSING SUMMARY")
        print(f"{'='*60}")
        
        total_files = len(results)
        total_chars = sum(r['characters'] for r in results)
        total_words = sum(r['words'] for r in results)
        total_sentences = sum(r['sentences'] for r in results)
        
        print(f"\nProcessed {total_files} files")
        print(f"Total characters: {total_chars:,}")
        print(f"Total words: {total_words:,}")
        print(f"Total sentences: {total_sentences:,}")
        print(f"Average words per file: {total_words/total_files:,.0f}")

# Example: Create and process a sample file
if __name__ == "__main__":
    # Create sample directory
    sample_dir = Path("sample_texts")
    sample_dir.mkdir(exist_ok=True)
    
    # Create sample text files
    sample_texts = {
        "sample1.txt": """Afaan Oromoo afaan Kushitikii kan dubbatamu Oromiyaa fi naannawa ishee keessatti dha.
Afaanichi afaan baayyinaan dubbatamu Afriikaa keessatti, Afrikaa Kibbaa fi Kaabaati.
Qubee sirna barreeffama Afaan Oromoo sirna Laatin irratti hundaa'e dha.""",
        
        "sample2.txt": """Oromiyaan biyya guddaa Afriikaa keessatti argamti.
Biyyichi baayyina ummataa fi ballina lafaatiin Afriikaa keessatti lammaffaa dha.
Oromiyaan naannoo biyyoo adda addaa wajjin dhadhaabdi.""",
        
        "sample3.txt": """Gadaa sirna haaraa hawaasaa Oromoo dha.
Sirnichii mooraa siyaasaa, dinagdee, hawaasaa fi aadaa of keessaa qaba.
Gadaa sirna demokraatawaa kan ture yeroo dheeraaf."""
    }
    
    # Write sample files
    for filename, content in sample_texts.items():
        filepath = sample_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created: {filepath}")
    
    # Process files
    processor = FileProcessor()
    print(f"\n{'='*60}")
    print("PROCESSING FILES")
    print(f"{'='*60}")
    
    results = processor.batch_process(sample_dir)
```

Run the file processor:
```bash
python file_processor.py
```

### Step 4: Interactive Exploration

Create `interactive_explorer.py`:

```python
#!/usr/bin/env python3
"""Interactive exploration of Qubee NLP."""

def explore_text():
    """Interactive text exploration."""
    
    print("=== Qubee NLP Interactive Explorer ===\n")
    print("Type Afaan Oromoo text to analyze it.")
    print("Commands: 'quit', 'help', 'examples'\n")
    
    while True:
        user_input = input("Enter text or command: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if user_input.lower() == 'help':
            print("\nAvailable commands:")
            print("  quit, exit, q - Exit the program")
            print("  help - Show this help message")
            print("  examples - Show example texts")
            print("\nOr enter Afaan Oromoo text to analyze it.")
            continue
        
        if user_input.lower() == 'examples':
            print("\nExample texts:")
            print("1. Afaan Oromoo afaan guddaa dha.")
            print("2. Oromiyaan biyya guddaa Afriikaa keessatti argamti.")
            print("3. Qubee sirna barreeffama Afaan Oromoo dha.")
            continue
        
        if not user_input:
            continue
        
        # Process the text
        from qubee_nlp import (
            validate_qubee_text,
            normalize_qubee,
            word_tokenize,
            sentence_tokenize
        )
        from qubee_nlp.alphabet import QubeeAlphabet, split_into_syllables
        
        print(f"\nAnalyzing: '{user_input}'")
        print("-" * 40)
        
        # Validate
        is_valid, invalid = validate_qubee_text(user_input)
        if not is_valid:
            print(f"✗ Invalid characters: {invalid}")
            continue
        
        print("✓ Text is valid Qubee")
        
        # Normalize
        normalized = normalize_qubee(user_input, preserve_case=True)
        print(f"✓ Normalized: '{normalized}'")
        
        # Tokenize
        words = word_tokenize(user_input, preserve_case=True)
        sentences = sentence_tokenize(user_input, preserve_case=True)
        
        print(f"✓ Words ({len(words)}): {words}")
        print(f"✓ Sentences ({len(sentences)}):")
        for i, sentence in enumerate(sentences, 1):
            print(f"  {i}. {sentence}")
        
        # Character analysis
        print("\nCharacter Analysis:")
        char_counts = {}
        for char in user_input.lower():
            if char.isalpha():
                char_counts[char] = char_counts.get(char, 0) + 1
        
        for char, count in sorted(char_counts.items()):
            is_vowel = QubeeAlphabet.is_vowel(char)
            is_consonant = QubeeAlphabet.is_consonant(char)
            char_type = "vowel" if is_vowel else "consonant" if is_consonant else "other"
            print(f"  '{char}': {count:2} times ({char_type})")
        
        # Syllable analysis for first word
        if words:
            first_word = words[0]
            syllables = split_into_syllables(first_word)
            print(f"\nSyllable analysis for '{first_word}': {syllables}")
        
        print()  # Empty line for readability

if __name__ == "__main__":
    explore_text()
```

Run the interactive explorer:
```bash
python interactive_explorer.py
```

## Common Tasks

### Task 1: Text Cleaning

```python
from qubee_nlp import normalize_qubee
from qubee_nlp.alphabet import validate_qubee_text

def clean_text(text):
    """Clean and normalize Afaan Oromoo text."""
    # Validate
    is_valid, invalid = validate_qubee_text(text)
    if not is_valid:
        # Remove invalid characters
        for char in invalid:
            text = text.replace(char, '')
    
    # Normalize
    cleaned = normalize_qubee(text)
    return cleaned

text = "  Áfáan   Oromoo  gúddáa   dha.  "
cleaned = clean_text(text)
print(f"Cleaned: '{cleaned}'")
```

### Task 2: Word Frequency Analysis

```python
from qubee_nlp import word_tokenize
from collections import Counter

def analyze_frequencies(text):
    """Analyze word frequencies in Afaan Oromoo text."""
    tokens = word_tokenize(text)
    freq = Counter(tokens)
    
    print(f"Total words: {len(tokens)}")
    print(f"Unique words: {len(freq)}")
    print("\nMost frequent words:")
    for word, count in freq.most_common(10):
        percentage = (count / len(tokens)) * 100
        print(f"  {word}: {count} ({percentage:.1f}%)")
    
    return freq

text = "Afaan Oromoo afaan guddaa dha. Oromiyaan biyya guddaa dha."
freq = analyze_frequencies(text)
```

### Task 3: Text Comparison

```python
from qubee_nlp import word_tokenize

def compare_texts(text1, text2):
    """Compare two Afaan Oromoo texts."""
    tokens1 = set(word_tokenize(text1))
    tokens2 = set(word_tokenize(text2))
    
    common = tokens1.intersection(tokens2)
    unique1 = tokens1 - tokens2
    unique2 = tokens2 - tokens1
    
    print(f"Text 1 unique words: {len(unique1)}")
    print(f"Text 2 unique words: {len(unique2)}")
    print(f"Common words: {len(common)}")
    
    similarity = len(common) / (len(tokens1) + len(tokens2) - len(common))
    print(f"Jaccard similarity: {similarity:.2f}")
    
    return {
        'common': sorted(common),
        'unique1': sorted(unique1),
        'unique2': sorted(unique2),
        'similarity': similarity
    }

text1 = "Afaan Oromoo afaan guddaa dha."
text2 = "Oromiyaan biyya guddaa dha."
compare_texts(text1, text2)
```

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'qubee_nlp'**
   ```bash
   # Make sure you installed the package
   pip install qubee-nlp
   
   # Or if installed in development mode
   pip install -e .
   ```

2. **UnicodeDecodeError when reading files**
   ```python
   # Always specify encoding
   with open('file.txt', 'r', encoding='utf-8') as f:
       text = f.read()
   ```

3. **Invalid characters error**
   ```python
   # Use validate_qubee_text to check
   from qubee_nlp.alphabet import validate_qubee_text
   is_valid, invalid = validate_qubee_text(your_text)
   print(f"Invalid characters: {invalid}")
   
   # Clean the text
   for char in invalid:
       your_text = your_text.replace(char, '')
   ```

4. **Performance issues with large texts**
   ```python
   # Process in chunks
   chunk_size = 10000  # characters
   for i in range(0, len(text), chunk_size):
       chunk = text[i:i+chunk_size]
       # Process chunk
   ```

## Next Steps

Now that you've completed this getting started guide:

1. **Explore Advanced Features**: Check out the other tutorials:
   - [Afaan Oromoo NLP](afaan_oromoo_nlp.md) - Advanced language-specific processing

2. **Read the API Documentation**:
   - [Alphabet Module](alphabet.md)
   - [Tokenizer Module](tokenizer.md)
   - [Stemmer Module](stemmer.md)
    - [Corpus Module](corpus.md)


3. **Try the Example Scripts**:
   - [Basic Usage](https://github.com/GUUTA/qubee-nlp/blob/main/examples/basic_usage.py)
   - [Tokenization Example](https://github.com/GUUTA/qubee-nlp/blob/main/examples/tokenization_example.py)
   - [Stemming Example](https://github.com/GUUTA/qubee-nlp/blob/main/examples/stemming_example.py)
   - [Advanced Features](https://github.com/GUUTA/qubee-nlp/blob/main/examples/advanced_features.py)
   

4. **Work with Real Data**: Try processing real Afaan Oromoo texts from:
   - Oromo news websites
   - Wikipedia articles in Afaan Oromoo
   - Oromo literature
   - Social media posts in Afaan Oromoo

5. **Contribute to the Project**: 
   - Report issues on GitHub
   - Suggest new features
   - Contribute code improvements

## Getting Help
   -  **GitHub Issues**: [Report bugs or request features](https://github.com/GUUTA/qubee-nlp/issues)
   - **Documentation**: Check the [API documentation](./api/) for detailed information
   - **Examples**: Look at the [examples directory](https://github.com/GUUTA/qubee-nlp/tree/main/examples) for working code
   - **Email**: [guutatesema@gmail.com](mailto:guutatesema@gmail.com)


Happy coding with Afaan Oromoo NLP! 🌍📚
```

This `getting_started.md` file provides a comprehensive tutorial covering:

1. **Installation** - Multiple installation methods
2. **Basic Concepts** - Understanding Qubee script and alphabet
3. **Step-by-Step Tutorials** - From simple scripts to file processing
4. **Interactive Tools** - For hands-on exploration
5. **Common Tasks** - Practical examples for real-world use
6. **Troubleshooting** - Solutions to common problems
7. **Next Steps** - Guidance for further learning

The tutorial is designed to be beginner-friendly while covering all essential aspects of using Qubee NLP for Afaan Oromoo text processing.