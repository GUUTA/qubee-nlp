#!/usr/bin/env python3
"""
Stemming and morphological analysis examples for Afaan Oromoo.
"""

from qubee_nlp import QubeeTokenizer
from qubee_nlp.stemmer import QubeeStemmer, get_affixes

def demonstrate_stemming():
    """Show stemming examples for Afaan Oromoo."""
    
    print("=== Stemming Examples for Afaan Oromoo ===\n")
    
    # Initialize stemmer
    stemmer = QubeeStemmer()
    tokenizer = QubeeTokenizer(preserve_case=False)
    
    # Example words with their stems
    examples = [
        # (word, expected_stem, description)
        ("barreessuu", "bar", "verb: to write"),
        ("barreessaan", "bar", "noun: writer"),
        ("barreessitoota", "bar", "plural noun: writers"),
        ("dubbachuu", "dub", "verb: to speak"),
        ("dubbachoota", "dub", "noun: speakers"),
        ("guddina", "gud", "noun: growth"),
        ("guddisuu", "gud", "verb: to grow something"),
        ("qabxii", "qab", "noun: chapter"),
        ("qabxiiwwan", "qab", "plural noun: chapters"),
        ("jiraachuu", "jir", "verb: to live"),
        ("jiraatoota", "jir", "noun: inhabitants"),
    ]
    
    print("Word Stemming Results:")
    print("-" * 50)
    for word, expected_stem, description in examples:
        stem = stemmer.stem(word)
        affixes = get_affixes(word, stem)
        
        print(f"\nWord: {word}")
        print(f"  Description: {description}")
        print(f"  Stem: {stem}")
        print(f"  Expected stem: {expected_stem}")
        print(f"  Match: {'✓' if stem == expected_stem else '✗'}")
        print(f"  Affixes: {affixes}")
    
    # Sentence stemming
    print("\n=== Sentence Stemming ===\n")
    
    sentences = [
        "Barreessitootni kitaaba bareessan.",
        "Oromoon Afaan Oromootiin dubbatu.",
        "Guddinni biyyaa akkaataa sirriitti itti fufe.",
    ]
    
    for sentence in sentences:
        tokens = tokenizer.tokenize(sentence)
        stems = [stemmer.stem(token) for token in tokens]
        
        print(f"Sentence: {sentence}")
        print(f"Tokens: {tokens}")
        print(f"Stems: {stems}")
        print()

def demonstrate_affix_analysis():
    """Show affix analysis examples."""
    
    print("=== Affix Analysis ===\n")
    
    from qubee_nlp.stemmer import analyze_word
    
    words = [
        "barreessuu",      # to write
        "barreessitoota",  # writers
        "dubbachuuf",      # in order to speak
        "jiraachuuf",      # in order to live
        "guddisuuf",       # in order to grow
    ]
    
    for word in words:
        analysis = analyze_word(word)
        print(f"\nWord: {word}")
        print(f"  Stem: {analysis['stem']}")
        print(f"  Prefixes: {analysis['prefixes']}")
        print(f"  Suffixes: {analysis['suffixes']}")
        print(f"  Root: {analysis['root']}")
        print(f"  Word type: {analysis['word_type']}")

def demonstrate_morphological_patterns():
    """Show common morphological patterns in Afaan Oromoo."""
    
    print("=== Morphological Patterns ===\n")
    
    # Common verb patterns
    verb_patterns = [
        ("bar", ["barreessuu", "barreessituu", "barreessaa"]),
        ("dub", ["dubbachuu", "dubbattu", "dubbata"]),
        ("jir", ["jiraachuu", "jiraatu", "jiraata"]),
        ("gud", ["guddisuu", "guddiftuu", "guddifa"]),
    ]
    
    print("Verb Conjugation Patterns:")
    for root, forms in verb_patterns:
        print(f"\nRoot: {root}")
        for form in forms:
            print(f"  {form}")
    
    # Noun patterns
    noun_patterns = [
        ("bar", ["barreessaa", "barreessitoota", "barreessaan"]),
        ("dub", ["dubbachaa", "dubbachoota", "dubbattaa"]),
        ("gud", ["guddina", "guddinaa", "guddisaa"]),
    ]
    
    print("\n\nNoun Derivation Patterns:")
    for root, forms in noun_patterns:
        print(f"\nRoot: {root}")
        for form in forms:
            print(f"  {form}")

if __name__ == "__main__":
    demonstrate_stemming()
    demonstrate_affix_analysis()
    demonstrate_morphological_patterns()