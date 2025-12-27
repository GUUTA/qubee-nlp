"""
Advanced validation utilities for Afaan Oromoo text.
"""

import re
from typing import Dict, List, Tuple, Set, Optional, Any
from collections import Counter
from ..alphabet import QubeeAlphabet


def validate_text(text: str, 
                  check_level: str = 'basic') -> Dict[str, Any]:
    """
    Comprehensive text validation for Afaan Oromoo.
    
    Args:
        text: Text to validate
        check_level: Validation level ('basic', 'strict', 'full')
        
    Returns:
        Dictionary with validation results
    """
    results = {
        'is_valid': True,
        'errors': [],
        'warnings': [],
        'statistics': {},
        'invalid_characters': [],
        'invalid_words': []
    }
    
    # Basic character validation
    is_valid, invalid_chars = QubeeAlphabet.validate_qubee_text(text, strict=(check_level == 'strict'))
    if not is_valid:
        results['is_valid'] = False
        results['invalid_characters'] = invalid_chars
        results['errors'].append(f"Invalid characters found: {invalid_chars}")
    
    # Word-level validation for strict and full checks
    if check_level in ['strict', 'full']:
        words = text.split()
        invalid_words = []
        
        for word in words:
            if not _is_valid_afaan_oromoo_word(word, check_level):
                invalid_words.append(word)
        
        if invalid_words:
            results['warnings'].append(f"Potentially invalid words: {invalid_words}")
            results['invalid_words'] = invalid_words
    
    # Phonotactic checks for full validation
    if check_level == 'full':
        phonotactic_issues = _check_phonotactic_rules(text)
        if phonotactic_issues:
            results['warnings'].extend(phonotactic_issues)
    
    # Calculate statistics
    results['statistics'] = calculate_text_metrics(text)
    
    return results


def validate_word(word: str, 
                  check_vowels: bool = True,
                  check_consonants: bool = True) -> Tuple[bool, List[str]]:
    """
    Validate a single Afaan Oromoo word.
    
    Args:
        word: Word to validate
        check_vowels: Whether to check vowel harmony
        check_consonants: Whether to check consonant clusters
        
    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []
    
    # Basic character validation
    is_valid, invalid_chars = QubeeAlphabet.validate_qubee_text(word, strict=True)
    if not is_valid:
        issues.append(f"Invalid characters: {invalid_chars}")
        return False, issues
    
    # Check word length
    if len(word) < 1:
        issues.append("Word is empty")
        return False, issues
    
    # Check for at least one vowel
    if not any(QubeeAlphabet.is_vowel(c) for c in word):
        issues.append("Word contains no vowels")
        return False, issues
    
    # Check vowel harmony (for strict validation)
    if check_vowels:
        harmony_issue = _check_vowel_harmony(word)
        if harmony_issue:
            issues.append(harmony_issue)
    
    # Check consonant clusters
    if check_consonants:
        cluster_issues = _check_consonant_clusters(word)
        issues.extend(cluster_issues)
    
    # Check for invalid sequences
    sequence_issues = _check_invalid_sequences(word)
    issues.extend(sequence_issues)
    
    return len(issues) == 0, issues


def check_phonotactics(text: str) -> List[str]:
    """
    Check phonotactic rules for Afaan Oromoo text.
    
    Args:
        text: Text to check
        
    Returns:
        List of phonotactic issues
    """
    issues = []
    words = text.split()
    
    for word in words:
        # Check word-initial constraints
        if len(word) >= 2:
            # Words shouldn't start with certain consonant clusters
            if (QubeeAlphabet.is_consonant(word[0]) and 
                QubeeAlphabet.is_consonant(word[1]) and
                word[0:2].upper() not in QubeeAlphabet.DIGRAPHS):
                # Some initial clusters are allowed, add specific rules here
                pass
        
        # Check vowel sequences
        for i in range(len(word) - 1):
            if (QubeeAlphabet.is_vowel(word[i]) and 
                QubeeAlphabet.is_vowel(word[i + 1])):
                vowel_pair = word[i:i+2].upper()
                if vowel_pair not in QubeeAlphabet.DIPHTHONGS:
                    issues.append(f"Uncommon vowel sequence '{vowel_pair}' in word '{word}'")
    
    return issues


def is_valid_syllable(syllable: str) -> bool:
    """
    Check if a syllable follows Afaan Oromoo syllable structure.
    
    Args:
        syllable: Syllable to check
        
    Returns:
        True if valid syllable structure
    """
    # Common syllable patterns in Afaan Oromoo: V, CV, CVC, VC
    pattern = re.compile(r'^([BCDFGHJKLMNPQRSTVWXYZ]?[AEIOUÁÉÍÓÚ][BCDFGHJKLMNPQRSTVWXYZ]?)$', re.IGNORECASE)
    return bool(pattern.match(syllable))


def calculate_text_metrics(text: str) -> Dict[str, Any]:
    """
    Calculate various text metrics for Afaan Oromoo text.
    
    Args:
        text: Text to analyze
        
    Returns:
        Dictionary with text metrics
    """
    # Tokenize (simple split for now)
    words = [w for w in text.split() if w]
    sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
    
    # Character statistics
    chars = len(text)
    letters = sum(1 for c in text if c.isalpha())
    spaces = text.count(' ')
    
    # Word statistics
    word_count = len(words)
    unique_words = len(set(words))
    
    # Sentence statistics
    sentence_count = len(sentences)
    
    # Calculate Type-Token Ratio (lexical diversity)
    ttr = unique_words / word_count if word_count > 0 else 0
    
    # Calculate average word length
    avg_word_length = sum(len(w) for w in words) / word_count if word_count > 0 else 0
    
    # Calculate average sentence length
    avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
    
    # Vowel/Consonant ratio
    vowels = sum(1 for c in text if QubeeAlphabet.is_vowel(c))
    consonants = sum(1 for c in text if QubeeAlphabet.is_consonant(c))
    vc_ratio = vowels / consonants if consonants > 0 else 0
    
    return {
        'characters': chars,
        'letters': letters,
        'spaces': spaces,
        'words': word_count,
        'unique_words': unique_words,
        'sentences': sentence_count,
        'type_token_ratio': ttr,
        'avg_word_length': avg_word_length,
        'avg_sentence_length': avg_sentence_length,
        'vowels': vowels,
        'consonants': consonants,
        'vowel_consonant_ratio': vc_ratio,
        'word_frequency': dict(Counter(words).most_common(10))
    }


def _is_valid_afaan_oromoo_word(word: str, check_level: str) -> bool:
    """
    Internal function to validate Afaan Oromoo word.
    """
    # Remove diacritics for checking
    word_normalized = QubeeAlphabet.normalize_diacritics(word).upper()
    
    # Check for invalid character sequences
    invalid_sequences = ['BB', 'CC', 'DD', 'FF', 'GG', 'JJ', 'KK', 'LL', 
                        'MM', 'NN', 'PP', 'QQ', 'RR', 'SS', 'TT', 'VV',
                        'WW', 'XX', 'YY', 'ZZ']
    
    for seq in invalid_sequences:
        if seq in word_normalized:
            return False
    
    # Check for vowel harmony in strict mode
    if check_level == 'strict':
        vowels = [c for c in word_normalized if QubeeAlphabet.is_vowel(c)]
        if vowels:
            # Check front/back vowel harmony
            front_vowels = {'E', 'I'}
            back_vowels = {'A', 'O', 'U'}
            
            has_front = any(v in front_vowels for v in vowels)
            has_back = any(v in back_vowels for v in vowels)
            
            # In strict Oromo, words typically don't mix front and back vowels
            if has_front and has_back:
                return False
    
    return True


def _check_vowel_harmony(word: str) -> Optional[str]:
    """
    Check vowel harmony in a word.
    
    Returns:
        Error message or None if valid
    """
    vowels = [c.upper() for c in word if QubeeAlphabet.is_vowel(c)]
    
    if not vowels:
        return None
    
    # Afaan Oromoo vowel harmony groups
    front_vowels = {'E', 'I', 'É', 'Í'}
    back_vowels = {'A', 'O', 'U', 'Á', 'Ó', 'Ú'}
    neutral_vowels = set()  # Some vowels might be neutral
    
    has_front = any(v in front_vowels for v in vowels)
    has_back = any(v in back_vowels for v in vowels)
    
    if has_front and has_back:
        # Check if it's a valid mixed vowel word
        # Some words in Afaan Oromoo can have mixed vowels
        common_mixed_words = {'akkas', 'akkana', 'amma'}
        if word.lower() not in common_mixed_words:
            return f"Word '{word}' mixes front and back vowels"
    
    return None


def _check_consonant_clusters(word: str) -> List[str]:
    """
    Check for invalid consonant clusters.
    
    Returns:
        List of issues
    """
    issues = []
    word_upper = word.upper()
    
    # Check for invalid initial clusters
    if len(word_upper) >= 2:
        initial_pair = word_upper[0:2]
        if (QubeeAlphabet.is_consonant(word_upper[0]) and 
            QubeeAlphabet.is_consonant(word_upper[1])):
            
            # List of allowed initial clusters in Afaan Oromoo
            allowed_initial_clusters = {'BR', 'DR', 'FR', 'GR', 'KR', 'PR', 'TR', 'SR'}
            if initial_pair not in allowed_initial_clusters:
                issues.append(f"Uncommon initial consonant cluster '{initial_pair}'")
    
    # Check for invalid medial clusters
    for i in range(1, len(word_upper) - 2):
        if (QubeeAlphabet.is_consonant(word_upper[i]) and 
            QubeeAlphabet.is_consonant(word_upper[i + 1]) and
            QubeeAlphabet.is_consonant(word_upper[i + 2])):
            cluster = word_upper[i:i+3]
            issues.append(f"Three-consonant cluster '{cluster}' might be invalid")
    
    return issues


def _check_invalid_sequences(word: str) -> List[str]:
    """
    Check for sequences that are invalid in Afaan Oromoo.
    
    Returns:
        List of issues
    """
    issues = []
    word_upper = word.upper()
    
    # Invalid sequences
    invalid_sequences = [
        'BM', 'BN', 'BP', 'BV',  # Rare/unlikely sequences
        'DM', 'DN', 'DP', 'DV',
        'GM', 'GN', 'GP', 'GV',
        'HM', 'HN', 'HP', 'HV',
        'JM', 'JN', 'JP', 'JV',
        'KM', 'KN', 'KP', 'KV',
        'LM', 'LN', 'LP', 'LV',
        'PM', 'PN', 'PP', 'PV',
        'QM', 'QN', 'QP', 'QV',
        'TM', 'TN', 'TP', 'TV',
        'VM', 'VN', 'VP', 'VV',
        'XM', 'XN', 'XP', 'XV',
        'ZM', 'ZN', 'ZP', 'ZV',
    ]
    
    for seq in invalid_sequences:
        if seq in word_upper:
            issues.append(f"Invalid sequence '{seq}' found")
    
    return issues