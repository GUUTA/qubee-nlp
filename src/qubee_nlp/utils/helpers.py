"""
Helper functions for Afaan Oromoo NLP processing.
"""

import re
from typing import List, Dict, Tuple, Set, Optional, Counter as CounterType
from collections import Counter
from ..alphabet import QubeeAlphabet, normalize_qubee


def normalize_text(text: str, 
                   preserve_case: bool = False,
                   remove_diacritics: bool = False,
                   collapse_spaces: bool = True) -> str:
    """
    Normalize text with multiple options.
    
    Args:
        text: Text to normalize
        preserve_case: Whether to preserve original case
        remove_diacritics: Whether to remove diacritics
        collapse_spaces: Whether to collapse multiple spaces
        
    Returns:
        Normalized text
    """
    normalized = text
    
    # Remove diacritics if requested
    if remove_diacritics:
        normalized = QubeeAlphabet.normalize_diacritics(normalized)
    
    # Normalize using main function (handles case and spaces)
    normalized = normalize_qubee(normalized, preserve_case=preserve_case)
    
    # Collapse spaces if requested
    if collapse_spaces:
        normalized = re.sub(r'\s+', ' ', normalized).strip()
    
    return normalized


def remove_diacritics(text: str) -> str:
    """
    Remove diacritics from text.
    
    Args:
        text: Text with possible diacritics
        
    Returns:
        Text without diacritics
    """
    return QubeeAlphabet.normalize_diacritics(text)


def count_syllables(word: str) -> int:
    """
    Count syllables in an Afaan Oromoo word.
    
    Args:
        word: Word to count syllables in
        
    Returns:
        Number of syllables
    """
    word = word.upper()
    syllable_count = 0
    i = 0
    
    while i < len(word):
        char = word[i]
        
        # Each vowel typically indicates a syllable
        if QubeeAlphabet.is_vowel(char):
            syllable_count += 1
            i += 1
        elif QubeeAlphabet.is_consonant(char):
            # Check for digraphs
            if i < len(word) - 1:
                digraph = char + word[i + 1]
                if digraph in QubeeAlphabet.DIGRAPHS:
                    i += 2
                    continue
            i += 1
        else:
            i += 1
    
    # Ensure at least one syllable
    return max(1, syllable_count)


def get_word_frequency(text: str, 
                       top_n: int = 20,
                       normalize: bool = True) -> List[Tuple[str, int]]:
    """
    Get word frequency from text.
    
    Args:
        text: Text to analyze
        top_n: Number of top words to return
        normalize: Whether to normalize words before counting
        
    Returns:
        List of (word, frequency) tuples sorted by frequency
    """
    # Tokenize (simple split for now)
    words = text.split()
    
    if normalize:
        words = [normalize_qubee(w, preserve_case=False) for w in words]
    
    # Count frequencies
    freq_counter = Counter(words)
    
    # Return top N words
    return freq_counter.most_common(top_n)


def split_by_sentence(text: str) -> List[str]:
    """
    Split text into sentences using Afaan Oromoo-specific rules.
    
    Args:
        text: Text to split
        
    Returns:
        List of sentences
    """
    # Common sentence endings in Afaan Oromoo
    sentence_endings = r'[.!?؟…]+'
    
    # Split by sentence endings
    sentences = re.split(sentence_endings, text)
    
    # Clean up sentences
    clean_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            clean_sentences.append(sentence)
    
    return clean_sentences


def calculate_ttr(text: str, window: Optional[int] = None) -> float:
    """
    Calculate Type-Token Ratio (lexical diversity).
    
    Args:
        text: Text to analyze
        window: If provided, calculate moving average TTR
        
    Returns:
        Type-Token Ratio
    """
    words = text.split()
    
    if not words:
        return 0.0
    
    if window is None:
        # Overall TTR
        unique_words = len(set(words))
        total_words = len(words)
        return unique_words / total_words if total_words > 0 else 0.0
    else:
        # Moving average TTR
        ttr_values = []
        for i in range(0, len(words) - window + 1):
            window_words = words[i:i + window]
            unique_in_window = len(set(window_words))
            ttr_values.append(unique_in_window / window)
        
        return sum(ttr_values) / len(ttr_values) if ttr_values else 0.0


def find_ngrams(text: str, n: int = 2) -> List[Tuple[str, ...]]:
    """
    Find n-grams in text.
    
    Args:
        text: Text to analyze
        n: Size of n-grams (2 for bigrams, 3 for trigrams, etc.)
        
    Returns:
        List of n-grams
    """
    words = text.split()
    
    if len(words) < n:
        return []
    
    ngrams = []
    for i in range(len(words) - n + 1):
        ngram = tuple(words[i:i + n])
        ngrams.append(ngram)
    
    return ngrams


def find_repeated_patterns(text: str, min_length: int = 3) -> Dict[str, int]:
    """
    Find repeated character patterns in text.
    
    Args:
        text: Text to analyze
        min_length: Minimum pattern length to consider
        
    Returns:
        Dictionary of patterns and their counts
    """
    patterns = {}
    text_lower = text.lower()
    
    for length in range(min_length, len(text_lower) // 2 + 1):
        for i in range(len(text_lower) - length + 1):
            pattern = text_lower[i:i + length]
            
            # Count occurrences
            count = text_lower.count(pattern)
            
            if count > 1:
                patterns[pattern] = count
    
    # Filter to only keep non-overlapping patterns
    filtered_patterns = {}
    sorted_patterns = sorted(patterns.items(), key=lambda x: (-len(x[0]), -x[1]))
    used_positions = set()
    
    for pattern, count in sorted_patterns:
        positions = []
        pos = text_lower.find(pattern)
        
        while pos != -1:
            # Check if this position overlaps with already used positions
            overlap = False
            for p in range(pos, pos + len(pattern)):
                if p in used_positions:
                    overlap = True
                    break
            
            if not overlap:
                positions.append(pos)
                for p in range(pos, pos + len(pattern)):
                    used_positions.add(p)
            
            pos = text_lower.find(pattern, pos + 1)
        
        if len(positions) > 1:
            filtered_patterns[pattern] = len(positions)
    
    return filtered_patterns


def extract_phrases(text: str, 
                    min_words: int = 2,
                    max_words: int = 4) -> Dict[str, int]:
    """
    Extract repeating phrases from text.
    
    Args:
        text: Text to analyze
        min_words: Minimum words in phrase
        max_words: Maximum words in phrase
        
    Returns:
        Dictionary of phrases and their frequencies
    """
    words = text.split()
    phrases = {}
    
    for phrase_length in range(min_words, max_words + 1):
        for i in range(len(words) - phrase_length + 1):
            phrase = ' '.join(words[i:i + phrase_length])
            phrases[phrase] = phrases.get(phrase, 0) + 1
    
    # Filter to only keep phrases that appear multiple times
    return {phrase: count for phrase, count in phrases.items() if count > 1}


def calculate_readability_score(text: str) -> Dict[str, float]:
    """
    Calculate readability scores for Afaan Oromoo text.
    
    Args:
        text: Text to analyze
        
    Returns:
        Dictionary with readability metrics
    """
    sentences = split_by_sentence(text)
    words = text.split()
    
    num_sentences = len(sentences)
    num_words = len(words)
    
    # Count syllables
    num_syllables = sum(count_syllables(word) for word in words)
    
    # Calculate averages
    avg_words_per_sentence = num_words / num_sentences if num_sentences > 0 else 0
    avg_syllables_per_word = num_syllables / num_words if num_words > 0 else 0
    
    # Simple readability scores (adapted for Afaan Oromoo)
    flesch_score = 206.835 - (1.015 * avg_words_per_sentence) - (84.6 * avg_syllables_per_word)
    
    # Adjust for Afaan Oromoo (these are rough estimates)
    if flesch_score > 90:
        readability_level = "Very Easy"
    elif flesch_score > 80:
        readability_level = "Easy"
    elif flesch_score > 70:
        readability_level = "Fairly Easy"
    elif flesch_score > 60:
        readability_level = "Standard"
    elif flesch_score > 50:
        readability_level = "Fairly Difficult"
    elif flesch_score > 30:
        readability_level = "Difficult"
    else:
        readability_level = "Very Difficult"
    
    return {
        'flesch_score': flesch_score,
        'readability_level': readability_level,
        'avg_words_per_sentence': avg_words_per_sentence,
        'avg_syllables_per_word': avg_syllables_per_word,
        'num_sentences': num_sentences,
        'num_words': num_words,
        'num_syllables': num_syllables
    }


def clean_text(text: str, 
               remove_punctuation: bool = False,
               remove_numbers: bool = False,
               remove_extra_spaces: bool = True) -> str:
    """
    Clean text by removing various elements.
    
    Args:
        text: Text to clean
        remove_punctuation: Whether to remove punctuation
        remove_numbers: Whether to remove numbers
        remove_extra_spaces: Whether to remove extra spaces
        
    Returns:
        Cleaned text
    """
    cleaned = text
    
    if remove_punctuation:
        # Keep only letters, spaces, and basic Afaan Oromoo characters
        cleaned = re.sub(r'[^\w\s\'\-]', ' ', cleaned)
    
    if remove_numbers:
        cleaned = re.sub(r'\d+', ' ', cleaned)
    
    if remove_extra_spaces:
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    return cleaned