#!/usr/bin/env python3
"""
Advanced features and integration examples for Qubee NLP.
"""

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

def demonstrate_stopword_removal():
    """Show stopword removal and text cleaning."""
    
    print("=== Stopword Removal ===\n")
    
    # Get Afaan Oromoo stopwords
    stopwords = get_stopwords(language='oromo')
    print(f"Number of stopwords: {len(stopwords)}")
    print(f"First 10 stopwords: {list(stopwords)[:10]}\n")
    
    # Example text with stopwords
    texts = [
        "Afaan Oromoo afaan guddaa Oromiyaati.",
        "Kuni kitaaba bareessuu dha.",
        "Ani Oromiyaa keessa jiraadha.",
    ]
    
    for text in texts:
        cleaned = remove_stopwords(text, language='oromo')
        print(f"Original: {text}")
        print(f"Cleaned: {cleaned}")
        print()

def demonstrate_pos_tagging():
    """Demonstrate part-of-speech tagging."""
    
    print("=== Part-of-Speech Tagging ===\n")
    
    # Initialize tagger
    tagger = POSTagger()
    
    # Sample sentences
    sentences = [
        "Oromoon Afaan Oromootiin dubbatu.",
        "Kitaabni bareessaan barreesse.",
        "Biyyiin Oromiyaa guddaa dha.",
    ]
    
    tokenizer = QubeeTokenizer()
    
    for sentence in sentences:
        tokens = tokenizer.tokenize(sentence)
        tags = tagger.tag(tokens)
        
        print(f"Sentence: {sentence}")
        print("Tokens and POS tags:")
        for token, tag in zip(tokens, tags):
            tag_name = get_afaan_oromoo_tags().get(tag, tag)
            print(f"  {token:15} -> {tag:5} ({tag_name})")
        print()

def demonstrate_advanced_normalization():
    """Show advanced text normalization features."""
    
    print("=== Advanced Normalization ===\n")
    
    normalizer = AdvancedNormalizer()
    
    # Text with various issues
    texts = [
        "  Áfáan   OROMOO    gúddáa   dha.  ",  # Mixed case, diacritics, extra spaces
        "Oromiyaa's biyya' guddaa' dha.",        # Apostrophe issues
        "Afaan-Oromoo afaan jalqaba-dha.",       # Hyphen handling
    ]
    
    for text in texts:
        normalized = normalizer.normalize(text)
        print(f"Original: '{text}'")
        print(f"Normalized: '{normalized}'")
        print()

def demonstrate_text_analysis_pipeline():
    """Complete text analysis pipeline."""
    
    print("=== Complete Text Analysis Pipeline ===\n")
    
    # Sample text
    text = """
    Afaan Oromoo afaan Kushitikii kan dubbatamu Oromiyaa fi naannawa ishee keessatti dha.
    Afaanichi afaan baayyinaan dubbatamu Afriikaa keessatti, Afrikaa Kibbaa fi Kaabaati.
    Qubee sirna barreeffama Afaan Oromoo sirna Laatin irratti hundaa'e dha.
    """
    
    print("Original Text:")
    print(text)
    print("-" * 60)
    
    # Step 1: Validation
    is_valid, invalid_chars = validate_qubee_text(text)
    print(f"\n1. Validation:")
    print(f"   Valid: {is_valid}")
    if invalid_chars:
        print(f"   Invalid characters: {invalid_chars}")
    
    # Step 2: Normalization
    normalized = normalize_qubee(text, preserve_case=True)
    print(f"\n2. Normalization:")
    print(f"   Normalized text: {normalized[:50]}...")
    
    # Step 3: Tokenization
    tokenizer = QubeeTokenizer(preserve_case=True)
    tokens = tokenizer.tokenize(normalized)
    print(f"\n3. Tokenization:")
    print(f"   Number of tokens: {len(tokens)}")
    print(f"   First 10 tokens: {tokens[:10]}")
    
    # Step 4: Stopword removal
    cleaned_tokens = [t for t in tokens if t.lower() not in get_stopwords('oromo')]
    print(f"\n4. Stopword Removal:")
    print(f"   Tokens after stopword removal: {len(cleaned_tokens)}")
    print(f"   Removed {len(tokens) - len(cleaned_tokens)} stopwords")
    
    # Step 5: POS Tagging
    tagger = POSTagger()
    if cleaned_tokens:
        tags = tagger.tag(cleaned_tokens[:10])  # Tag first 10 for demo
        print(f"\n5. POS Tagging (first 10):")
        for token, tag in zip(cleaned_tokens[:10], tags):
            print(f"   {token:15} -> {tag}")
    
    # Step 6: Frequency analysis
    from collections import Counter
    freq = Counter(cleaned_tokens)
    print(f"\n6. Frequency Analysis:")
    print(f"   Most common words:")
    for word, count in freq.most_common(5):
        print(f"   {word:15}: {count}")
    
    # Step 7: Syllable analysis
    print(f"\n7. Syllable Analysis:")
    for i, word in enumerate(cleaned_tokens[:5], 1):
        syllables = split_into_syllables(word)
        print(f"   {word:15} -> {syllables}")

def demonstrate_custom_extensions():
    """Show how to extend the library with custom functionality."""
    
    print("=== Custom Extensions ===\n")
    
    # Custom token filter example
    class CustomTokenFilter:
        def __init__(self, min_length=3):
            self.min_length = min_length
            
        def filter(self, tokens):
            return [
                token for token in tokens 
                if len(token) >= self.min_length 
                and not token.isdigit()
            ]
    
    # Custom normalizer example
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
    
    # Usage examples
    tokenizer = QubeeTokenizer()
    text = "Waan isan jedhan inni sirrii dha."
    
    tokens = tokenizer.tokenize(text)
    print(f"Original tokens: {tokens}")
    
    # Apply custom filter
    custom_filter = CustomTokenFilter(min_length=4)
    filtered_tokens = custom_filter.filter(tokens)
    print(f"Filtered tokens (min length 4): {filtered_tokens}")
    
    # Apply dialect normalization
    dialect_normalizer = DialectNormalizer()
    normalized_text = dialect_normalizer.normalize(text)
    print(f"\nOriginal text: {text}")
    print(f"Dialect-normalized: {normalized_text}")

if __name__ == "__main__":
    demonstrate_stopword_removal()
    demonstrate_pos_tagging()
    demonstrate_advanced_normalization()
    demonstrate_text_analysis_pipeline()
    demonstrate_custom_extensions()