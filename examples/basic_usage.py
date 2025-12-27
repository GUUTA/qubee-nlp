#!/usr/bin/env python3
"""
Basic usage examples for Qubee NLP library for Afaan Oromoo.
"""

from qubee_nlp import (
    word_tokenize,
    sentence_tokenize,
    validate_qubee_text,
    normalize_qubee,
    QubeeAlphabet
)

def main():
    """Main function demonstrating basic usage."""
    
    print("=== Qubee NLP Basic Usage Examples ===\n")
    
    # Example 1: Text validation
    print("1. Text Validation:")
    texts = [
        "Afaan Oromoo afaan jalqaba Oromiyaati.",
        "Hello 123",  # Contains invalid characters
        "Áfáan Órómóó gúddáa dha.",  # With diacritics
    ]
    
    for text in texts:
        is_valid, invalid_chars = validate_qubee_text(text)
        status = "✓ Valid" if is_valid else f"✗ Invalid chars: {invalid_chars}"
        print(f"  '{text}' -> {status}")
    
    # Example 2: Word tokenization
    print("\n2. Word Tokenization:")
    text = "Oromiyaan biyya guddaa Afriikaa keessatti argamti."
    tokens = word_tokenize(text)
    print(f"  Text: {text}")
    print(f"  Tokens: {tokens}")
    
    # Example 3: Sentence tokenization
    print("\n3. Sentence Tokenization:")
    text = "Akkaataa dubbii kanaati. Barreeffama kun Afaan Oromoodha. Galatoomaa!"
    sentences = sentence_tokenize(text)
    print(f"  Text: {text}")
    print(f"  Sentences: {sentences}")
    
    # Example 4: Normalization
    print("\n4. Text Normalization:")
    text = "  Áfáan   Oromoo  gúddáa   dha.  "
    normalized = normalize_qubee(text)
    print(f"  Original: '{text}'")
    print(f"  Normalized: '{normalized}'")
    
    # Example 5: Alphabet utilities
    print("\n5. Alphabet Utilities:")
    test_chars = ['A', 'b', 'x', '1', 'á']
    for char in test_chars:
        is_vowel = QubeeAlphabet.is_vowel(char)
        is_consonant = QubeeAlphabet.is_consonant(char)
        is_letter = QubeeAlphabet.is_qubee_letter(char)
        print(f"  '{char}': vowel={is_vowel}, consonant={is_consonant}, letter={is_letter}")
    
    # Example 6: Processing a longer text
    print("\n6. Processing Longer Text:")
    long_text = """
    Afaan Oromoo afaan Kushitikii kan dubbatamu Oromiyaa fi naannawa ishee keessatti dha.
    Afaan Oromoo afaan baayyinaan dubbatamu Afriikaa keessatti, Afrikaa Kibbaa fi Kaabaati.
    Qubee sirna barreeffama Afaan Oromoo sirna Laatin irratti hundaa'e dha.
    """
    
    # Validate
    is_valid, invalid = validate_qubee_text(long_text)
    print(f"  Text is valid: {is_valid}")
    
    # Tokenize
    all_tokens = word_tokenize(long_text)
    unique_tokens = set(all_tokens)
    print(f"  Total tokens: {len(all_tokens)}")
    print(f"  Unique tokens: {len(unique_tokens)}")
    
    # Show first 10 tokens
    print(f"  First 10 tokens: {all_tokens[:10]}")

if __name__ == "__main__":
    main()