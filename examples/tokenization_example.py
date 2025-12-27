#!/usr/bin/env python3
"""
Advanced tokenization examples for Afaan Oromoo text.
"""

from qubee_nlp import QubeeTokenizer
from qubee_nlp.alphabet import split_into_syllables

def demonstrate_tokenization():
    """Show different tokenization approaches."""
    
    print("=== Advanced Tokenization Examples ===\n")
    
    # Create different tokenizers
    tokenizer_default = QubeeTokenizer(preserve_case=False, strict=False)
    tokenizer_preserve_case = QubeeTokenizer(preserve_case=True, strict=False)
    tokenizer_strict = QubeeTokenizer(preserve_case=False, strict=True)
    
    # Sample texts
    texts = [
        "Afaan Oromoo afaan jalqaba Oromiyaati.",
        "Áfáan Órómóó gúddáa dha!",
        "Waa'ee dubbiin kana: 'Qubee fura Afaan Oromoo barreessuudha' jedhamu.",
        "Dr. Abbaa Gadaa prof. dha; Oromiyaa keessa jiraata."
    ]
    
    for i, text in enumerate(texts, 1):
        print(f"\nExample {i}:")
        print(f"  Text: {text}")
        
        # Different tokenization methods
        tokens_default = tokenizer_default.tokenize(text)
        tokens_case = tokenizer_preserve_case.tokenize(text)
        
        print(f"  Default tokens: {tokens_default}")
        print(f"  Case-preserved tokens: {tokens_case}")
        
        # Tokenize with positions
        try:
            tokens_with_pos = tokenizer_default.tokenize_with_positions(text)
            print(f"  First 3 tokens with positions:")
            for token_info in tokens_with_pos[:3]:
                print(f"    {token_info}")
        except ValueError as e:
            print(f"  Error: {e}")
        
        # Sentence tokenization
        sentences = tokenizer_default.sentence_tokenize(text)
        print(f"  Sentences: {sentences}")
    
    # Syllable splitting examples
    print("\n=== Syllable Splitting Examples ===\n")
    
    words = ["Oromiyaa", "barreessuu", "dubbachuu", "guddina", "qabxii"]
    
    for word in words:
        syllables = split_into_syllables(word)
        print(f"  '{word}' -> {syllables}")
    
    # Tokenize with context
    print("\n=== Tokenization with Context ===\n")
    
    text = "Afaan Oromoo afaan guddaa dha."
    tokenizer = QubeeTokenizer()
    tokens_with_context = tokenizer.tokenize_with_context(text, context_chars=3)
    
    print(f"Text: {text}")
    print("Tokens with context:")
    for token_info in tokens_with_context:
        print(f"  Token: '{token_info['token']}'")
        print(f"    Left context: '{token_info['left_context']}'")
        print(f"    Right context: '{token_info['right_context']}'")
        print(f"    Is valid Afaan Oromoo: {token_info['is_valid_afaan_oromoo']}")

def benchmark_tokenization():
    """Simple tokenization benchmark."""
    import time
    
    print("\n=== Tokenization Benchmark ===\n")
    
    # Load some sample text
    sample_text = "Afaan Oromoo " * 1000  # Repeat 1000 times
    
    tokenizer = QubeeTokenizer()
    
    # Time word tokenization
    start_time = time.time()
    tokens = tokenizer.tokenize(sample_text)
    word_time = time.time() - start_time
    
    # Time sentence tokenization
    start_time = time.time()
    sentences = tokenizer.sentence_tokenize(sample_text)
    sentence_time = time.time() - start_time
    
    print(f"Text length: {len(sample_text)} characters")
    print(f"Number of tokens: {len(tokens)}")
    print(f"Word tokenization time: {word_time:.4f} seconds")
    print(f"Sentence tokenization time: {sentence_time:.4f} seconds")
    print(f"Tokens per second: {len(tokens) / word_time:.0f}")

if __name__ == "__main__":
    demonstrate_tokenization()
    benchmark_tokenization()