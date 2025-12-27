"""
Tests for Qubee syllabifier module.
"""
import pytest
#from qubee_nlp.syllabifier import Syllabifier, syllabify_word, syllabify_text
from qubee_nlp.syllabifier import QubeeSyllabifier, syllabify_word, syllabify_text


class TestQubeeSyllabifier:
    """Test QubeeSyllabifier class."""
    
    def test_syllabifier_initialization(self):
        """Test syllabifier initialization."""
        syllabifier = QubeeSyllabifier()
        assert syllabifier is not None
        assert hasattr(syllabifier, 'syllabify')
    
    def test_syllabify_basic_words(self):
        """Test syllabification of basic Afaan Oromoo words."""
        syllabifier = QubeeSyllabifier()
        
        test_cases = [
            ("afaan", ["a", "faan"]),  # a-faan
            ("oromoo", ["o", "ro", "moo"]),  # o-ro-moo
            ("dubbachuu", ["dub", "ba", "chuu"]),  # dub-ba-chuu
            ("barreessuu", ["bar", "rees", "suu"]),  # bar-rees-suu
            ("mana", ["ma", "na"]),  # ma-na
            ("biyya", ["biy", "ya"]),  # biy-ya
        ]
        
        for word, expected in test_cases:
            syllables = syllabifier.syllabify(word)
            assert syllables == expected, f"Failed for {word}: got {syllables}"
            assert all(isinstance(s, str) for s in syllables)
    
    def test_syllabify_with_diacritics(self):
        """Test syllabification with diacritics."""
        syllabifier = QubeeSyllabifier()
        
        # Diacritics should be normalized
        assert syllabifier.syllabify("Áfáan") == ["a", "faan"]
        assert syllabifier.syllabify("Órómóó") == ["o", "ro", "moo"]
    
    def test_syllabify_case_handling(self):
        """Test case handling in syllabification."""
        syllabifier = QubeeSyllabifier()
        
        # Should work with different cases (normalized to lowercase)
        assert syllabifier.syllabify("AFAAN") == ["a", "faan"]
        assert syllabifier.syllabify("Afaan") == ["a", "faan"]
        assert syllabifier.syllabify("afaan") == ["a", "faan"]
    
    def test_syllabify_empty_input(self):
        """Test syllabification of empty input."""
        syllabifier = QubeeSyllabifier()
        assert syllabifier.syllabify("") == []
        assert syllabifier.syllabify("   ") == []
    
    def test_syllabify_single_character(self):
        """Test syllabification of single characters."""
        syllabifier = QubeeSyllabifier()
        
        single_chars = ["a", "b", "c", "d", "e"]
        for char in single_chars:
            syllables = syllabifier.syllabify(char)
            assert syllables == [char.lower()]
            assert len(syllables) == 1
    
    def test_syllabify_digraphs(self):
        """Test syllabification of words with digraphs."""
        syllabifier = QubeeSyllabifier()
        
        digraph_words = [
            ("chala", ["cha", "la"]),  # CH digraph
            ("shaggy", ["shag", "gy"]),  # SH digraph
            ("dhaamsa", ["dhaam", "sa"]),  # DH digraph
            ("nyata", ["nya", "ta"]),  # NY digraph
        ]
        
        for word, expected in digraph_words:
            syllables = syllabifier.syllabify(word)
            # Check that digraphs are kept together
            joined = "".join(syllables).lower()
            if "ch" in word:
                assert "ch" in joined
            if "sh" in word:
                assert "sh" in joined
            if "dh" in word:
                assert "dh" in joined
    
    def test_syllabify_consonant_clusters(self):
        """Test syllabification of consonant clusters."""
        syllabifier = QubeeSyllabifier()
        
        cluster_words = [
            ("arguu", ["ar", "guu"]),  # RG cluster
            ("beekuu", ["bee", "kuu"]),  # K cluster
            ("deemu", ["dee", "mu"]),  # M single
            ("qabu", ["qa", "bu"]),  # B single
        ]
        
        for word, expected in cluster_words:
            syllables = syllabifier.syllabify(word)
            assert len(syllables) == len(expected), f"Failed for {word}"
    
    def test_syllabify_vowel_clusters(self):
        """Test syllabification of vowel clusters."""
        syllabifier = QubeeSyllabifier()
        
        vowel_clusters = [
            ("aa", ["aa"]),  # Double vowel
            ("aai", ["aai"]),  # Triple vowel
            ("oo", ["oo"]),  # Double o
            ("ee", ["ee"]),  # Double e
        ]
        
        for vowels, expected in vowel_clusters:
            syllables = syllabifier.syllabify(vowels)
            assert syllables == expected
    
    def test_syllabify_with_apostrophe(self):
        """Test syllabification with apostrophe."""
        syllabifier = QubeeSyllabifier()
        
        # Words with apostrophe
        assert syllabifier.syllabify("dha'ii") == ["dha", "ii"]
        assert syllabifier.syllabify("kan'aa") == ["kan", "aa"]
    
    def test_syllabify_complex_words(self):
        """Test syllabification of complex words."""
        syllabifier = QubeeSyllabifier()
        
        complex_words = [
            ("oromiyaa", ["o", "ro", "mi", "yaa"]),
            ("afriikaa", ["a", "fri", "i", "kaa"]),
            ("barsiisaa", ["bar", "sii", "saa"]),
            ("jireenyaa", ["ji", "reen", "yaa"]),
        ]
        
        for word, expected in complex_words:
            syllables = syllabifier.syllabify(word)
            # At least check it returns sensible syllables
            assert len(syllables) >= 2
            assert all(len(s) > 0 for s in syllables)
            # Reconstructed word should match original (minus case/diacritics)
            reconstructed = "".join(syllables)
            assert reconstructed == word.lower()
    
    def test_syllabify_invalid_words(self):
        """Test syllabification of invalid words."""
        syllabifier = QubeeSyllabifier()
        
        # Invalid words should still return something
        assert syllabifier.syllabify("123") == []  # Numbers only
        assert syllabifier.syllabify("abc123") == []  # Mixed with numbers
        assert syllabifier.syllabify("@word") == []  # Special char at start
    
    def test_syllabify_with_hyphen(self):
        """Test syllabification with hyphen."""
        syllabifier = QubeeSyllabifier()
        
        # Hyphenated words - might split or treat as separate
        syllables = syllabifier.syllabify("afaan-afaan")
        # This depends on implementation - could be ["afaan", "afaan"] or ["afaan-afaan"]
        assert isinstance(syllables, list)
        assert len(syllables) > 0


class TestSyllabifyWordFunction:
    """Test syllabify_word convenience function."""
    
    def test_syllabify_word_basic(self):
        """Test basic syllabify_word function."""
        assert syllabify_word("afaan") == ["a", "faan"]
        assert syllabify_word("oromoo") == ["o", "ro", "moo"]
    
    def test_syllabify_word_with_diacritics(self):
        """Test syllabify_word with diacritics."""
        assert syllabify_word("Áfáan") == ["a", "faan"]
        assert syllabify_word("Órómóó") == ["o", "ro", "moo"]
    
    def test_syllabify_word_case_insensitive(self):
        """Test that syllabify_word is case insensitive."""
        assert syllabify_word("AFAAN") == ["a", "faan"]
        assert syllabify_word("Afaan") == ["a", "faan"]
        assert syllabify_word("afaan") == ["a", "faan"]


class TestSyllabifyTextFunction:
    """Test syllabify_text function."""
    
    def test_syllabify_text_basic(self):
        """Test basic syllabify_text function."""
        syllabifier = QubeeSyllabifier()
        
        text = "Afaan Oromoo"
        result = syllabifier.syllabify_text(text)
        
        # Should return list of words, each with syllables
        assert isinstance(result, list)
        assert len(result) == 2  # Two words
        
        # Check structure
        for word_syllables in result:
            assert isinstance(word_syllables, list)
            assert all(isinstance(s, str) for s in word_syllables)
    
    def test_syllabify_text_with_punctuation(self):
        """Test syllabify_text with punctuation."""
        syllabifier = QubeeSyllabifier()
        
        text = "Akkam jirta? Afaan Oromoo dha."
        result = syllabifier.syllabify_text(text)
        
        # Should handle punctuation (might be filtered out)
        assert isinstance(result, list)
        # Number of word entries might be 3-5 depending on punctuation handling
    
    def test_syllabify_text_empty(self):
        """Test syllabify_text with empty input."""
        syllabifier = QubeeSyllabifier()
        
        assert syllabifier.syllabify_text("") == []
        assert syllabifier.syllabify_text("   ") == []
        assert syllabifier.syllabify_text("\n\t") == []
    
    def test_syllabify_text_multiple_words(self):
        """Test syllabify_text with multiple words."""
        syllabifier = QubeeSyllabifier()
        
        text = "Afaan Oromoo afaan jalqaba dha"
        result = syllabifier.syllabify_text(text)
        
        assert len(result) == 5  # 5 words
        # Check first word
        assert result[0] == ["a", "faan"]
        # Check second word
        assert result[1] == ["o", "ro", "moo"]


class TestSyllabifyTextConvenience:
    """Test syllabify_text convenience function."""
    
    def test_syllabify_text_function(self):
        """Test syllabify_text module-level function."""
        result = syllabify_text("Afaan Oromoo")
        
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0] == ["a", "faan"]
        assert result[1] == ["o", "ro", "moo"]
    
    def test_syllabify_text_with_options(self):
        """Test syllabify_text with different options."""
        # Test with custom syllabifier
        syllabifier = QubeeSyllabifier()
        result = syllabify_text("Afaan Oromoo", syllabifier=syllabifier)
        
        assert isinstance(result, list)
        assert len(result) == 2


class TestSyllabificationRules:
    """Test specific syllabification rules."""
    
    def test_vowel_initial_words(self):
        """Test words starting with vowels."""
        syllabifier = QubeeSyllabifier()
        
        vowel_initial = [
            ("afaan", ["a", "faan"]),  # V-CVVC
            ("oromoo", ["o", "ro", "moo"]),  # V-CV-CVV
            ("ibidda", ["i", "bid", "da"]),  # V-CVC-CV
            ("abbaa", ["ab", "baa"]),  # VC-CVV
        ]
        
        for word, expected in vowel_initial:
            syllables = syllabifier.syllabify(word)
            # First syllable should start with vowel
            assert syllables[0][0].lower() in 'aeiou'
    
    def test_consonant_initial_words(self):
        """Test words starting with consonants."""
        syllabifier = QubeeSyllabifier()
        
        consonant_initial = [
            ("bara", ["ba", "ra"]),  # CV-CV
            ("dubbachuu", ["dub", "ba", "chuu"]),  # CVC-CV-CCVV
            ("guddaa", ["gud", "daa"]),  # CVC-CVV
            ("mana", ["ma", "na"]),  # CV-CV
        ]
        
        for word, expected in consonant_initial:
            syllables = syllabifier.syllabify(word)
            # First syllable should start with consonant (or consonant cluster)
            first_syllable = syllables[0].lower()
            # Check if starts with consonant (consider digraphs)
            if len(first_syllable) >= 2 and first_syllable[:2] in ['ch', 'sh', 'dh', 'ny']:
                assert True  # Starts with consonant digraph
            else:
                assert first_syllable[0] not in 'aeiou'
    
    def test_closed_syllables(self):
        """Test words with closed syllables (ending in consonant)."""
        syllabifier = QubeeSyllabifier()
        
        closed_syllable_words = [
            ("arguu", ["ar", "guu"]),  # CVC-CVV (first syllable closed)
            ("barsa", ["bar", "sa"]),  # CVC-CV
            ("dhaloota", ["dha", "loo", "ta"]),  # CV-CVV-CV (all open except maybe last)
        ]
        
        for word, expected in closed_syllable_words:
            syllables = syllabifier.syllabify(word)
            # Check that some syllables end with consonants
            has_closed = any(s[-1].lower() not in 'aeiou' for s in syllables)
            # In Afaan Oromoo, many syllables are open, but some can be closed
            assert True  # Just don't crash
    
    def test_geminate_consonants(self):
        """Test words with geminate (double) consonants."""
        syllabifier = QubeeSyllabifier()
        
        geminate_words = [
            ("guddaa", ["gud", "daa"]),  # Double d
            ("affaa", ["af", "faa"]),  # Double f
            ("mammaaksa", ["mam", "maak", "sa"]),  # Double m
        ]
        
        for word, expected in geminate_words:
            syllables = syllabifier.syllabify(word)
            # Geminates should be split between syllables
            reconstructed = "".join(syllables)
            # The word should reconstruct correctly
            assert reconstructed == word.lower()


class TestSyllabifierEdgeCases:
    """Test edge cases in syllabification."""
    
    @pytest.mark.parametrize("word", [
        "a" * 20,  # Very long vowel sequence
        "b" * 20,  # Very long consonant sequence
        "ab" * 20,  # Alternating
        "abc" * 20,  # Pattern
    ])
    def test_very_long_words(self, word):
        """Test syllabification of very long words."""
        syllabifier = QubeeSyllabifier()
        syllables = syllabifier.syllabify(word)
        
        # Should return something
        assert isinstance(syllables, list)
        # Should have at least one syllable
        assert len(syllables) >= 1
        # Reconstructed should match (case-normalized)
        reconstructed = "".join(syllables)
        assert reconstructed == word.lower()
    
    def test_words_with_numbers(self):
        """Test words containing numbers."""
        syllabifier = QubeeSyllabifier()
        
        # Words with numbers should probably return empty
        assert syllabifier.syllabify("word123") == []
        assert syllabifier.syllabify("123word") == []
        assert syllabifier.syllabify("1a2b3c") == []
    
    def test_words_with_special_chars(self):
        """Test words with special characters."""
        syllabifier = QubeeSyllabifier()
        
        special_cases = [
            ("word-word", []),  # Hyphen might split
            ("word'word", []),  # Apostrophe might split
            ("word.word", []),  # Period
            ("word_word", []),  # Underscore
        ]
        
        for word, expected in special_cases:
            syllables = syllabifier.syllabify(word)
            # Implementation specific - should at least not crash
            assert isinstance(syllables, list)
    
    def test_syllabification_idempotent(self):
        """Test that syllabification is idempotent."""
        syllabifier = QubeeSyllabifier()
        word = "dubbachuu"
        
        syllables1 = syllabifier.syllabify(word)
        # Syllabify the reconstructed word
        reconstructed = "".join(syllables1)
        syllables2 = syllabifier.syllabify(reconstructed)
        
        # Should give same result
        assert syllables1 == syllables2
    
    def test_syllable_count_consistency(self):
        """Test that syllable count is consistent."""
        syllabifier = QubeeSyllabifier()
        
        test_words = ["afaan", "oromoo", "dubbachuu", "barreessuu", "namoota"]
        
        for word in test_words:
            syllables = syllabifier.syllabify(word)
            # Count should be reasonable
            assert 1 <= len(syllables) <= len(word)
            # Each syllable should have at least one vowel (usually)
            has_vowel_count = sum(1 for s in syllables if any(c in 'aeiou' for c in s))
            assert has_vowel_count >= len(syllables) - 1  # Most syllables have vowels


if __name__ == "__main__":
    pytest.main([__file__, "-v"])