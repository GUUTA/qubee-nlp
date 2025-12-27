import pytest
from qubee_nlp.alphabet import (
    QubeeAlphabet,
    validate_qubee_text,
    is_valid_qubee,
    normalize_qubee,
    split_into_syllables,
    is_valid_afaan_oromoo_word
)


class TestQubeeAlphabet:
    """Test QubeeAlphabet class methods."""
    
    def test_is_vowel(self):
        assert QubeeAlphabet.is_vowel('a') is True
        assert QubeeAlphabet.is_vowel('E') is True
        assert QubeeAlphabet.is_vowel('b') is False
        assert QubeeAlphabet.is_vowel('x') is False
        assert QubeeAlphabet.is_vowel('1') is False
    
    def test_is_consonant(self):
        assert QubeeAlphabet.is_consonant('b') is True
        assert QubeeAlphabet.is_consonant('X') is True
        assert QubeeAlphabet.is_consonant('a') is False
        assert QubeeAlphabet.is_consonant('E') is False
        assert QubeeAlphabet.is_consonant('@') is False
        assert QubeeAlphabet.is_consonant('5') is False
    
    def test_is_qubee_letter(self):
        assert QubeeAlphabet.is_qubee_letter('a') is True
        assert QubeeAlphabet.is_qubee_letter('Z') is True
        assert QubeeAlphabet.is_qubee_letter('1') is False
        assert QubeeAlphabet.is_qubee_letter('@') is False
    
    def test_normalize_diacritics(self):
        assert QubeeAlphabet.normalize_diacritics('Áfáan') == 'Afaan'
        assert QubeeAlphabet.normalize_diacritics('Órómóó') == 'Oromoo'
        assert QubeeAlphabet.normalize_diacritics('Káaffée') == 'Kaaffee'
        assert QubeeAlphabet.normalize_diacritics('ibidda') == 'ibidda'
        assert QubeeAlphabet.normalize_diacritics('ABC') == 'ABC'
    
    def test_get_all_letters(self):
        letters = QubeeAlphabet.get_all_letters()
        assert isinstance(letters, list)
        assert len(letters) == 26
        assert 'A' in letters
        assert 'Z' in letters
        assert 'X' in letters
        assert all(letter.isalpha() for letter in letters)
        assert letters == sorted(letters)


class TestValidateQubeeText:
    
    def test_validate_valid_text(self):
        valid_texts = [
            "Afaan Oromoo",
            "Oromiyaan biyya guddaa Afriikaa keessatti argamti",
            "Akkam jirta?",
            "Galatoomaa!",
            "Namoonni baay'een kan dubbatu.",
            "Barreeffama qubeen kan barreeffamudha."
        ]
        for text in valid_texts:
            is_valid, invalid_chars = validate_qubee_text(text)
            assert is_valid is True
            assert len(invalid_chars) == 0
    
    def test_validate_with_diacritics(self):
        text = "Áfáan Órómóó"
        is_valid, invalid_chars = validate_qubee_text(text)
        assert is_valid is True
        assert len(invalid_chars) == 0
    
    def test_validate_invalid_text(self):
        test_cases = [
            ("Oromo123", ['1', '2', '3']),
            ("Afaan@Oromoo", ['@']),
            ("Oromo#language", ['#']),
            ("Test$123", ['$', '1', '2', '3']),
        ]
        for text, expected_invalid in test_cases:
            is_valid, invalid_chars = validate_qubee_text(text)
            assert is_valid is False
            assert all(char in invalid_chars for char in expected_invalid)
    
    def test_validate_strict_mode(self):
        text = "Akkam jirta?"
        is_valid_strict, _ = validate_qubee_text(text, strict=True)
        is_valid_lenient, _ = validate_qubee_text(text, strict=False)
        assert is_valid_strict is False
        assert is_valid_lenient is True
    
    def test_is_valid_qubee(self):
        assert is_valid_qubee("Afaan Oromoo") is True
        assert is_valid_qubee("Oromo123") is False
        assert is_valid_qubee("Áfáan") is True
        assert is_valid_qubee("Test@123", strict=True) is False


class TestNormalizeQubee:
    
    def test_normalize_qubee_basic(self):
        assert normalize_qubee("  Afaan   Oromoo  ") == "AFAAN OROMOO"
        assert normalize_qubee("\tOromiyaa\n") == "OROMIYAA"
        assert normalize_qubee("  Biyya  guddaa  ") == "BIYYA GUDDAA"
    
    def test_normalize_with_diacritics(self):
        assert normalize_qubee("Áfáan Órómóó") == "AFAAN OROMOO"
        assert normalize_qubee("Cáffée íbidda") == "CAFFEE IBIDDA"
    
    def test_normalize_preserve_case(self):
        text = "Áfáan Oromoo"
        assert normalize_qubee(text, preserve_case=True) == "Afaan Oromoo"
        assert normalize_qubee(text, preserve_case=False) == "AFAAN OROMOO"
        assert normalize_qubee("AfAaN OrOmOo", preserve_case=True) == "AfAaN OrOmOo"
    
    def test_normalize_special_chars(self):
        assert normalize_qubee("dha'ii") == "DHA'II"
        assert normalize_qubee("afaan-afaan") == "AFAAN-AFAAN"
        assert normalize_qubee("afaan  oromoo   dha") == "AFAAN OROMOO DHA"


class TestSyllableSplitting:
    
    def test_split_into_syllables(self):
        test_cases = [
            ("afaan", ["A", "FAAN"]),
            ("oromoo", ["O", "RO", "MOO"]),
            ("dubbachuu", ["DUB", "BA", "CHUU"]),
            ("barreessuu", ["BAR", "REES", "SUU"]),
        ]
        for word, expected in test_cases:
            syllables = split_into_syllables(word)
            assert syllables == expected
    
    def test_split_digraph_words(self):
        test_cases = [
            ("chaalaa", ["CHAA", "LAA"]),
            ("shagaa", ["SHA", "GAA"]),
            ("dhaamsa", ["DHAAM", "SA"]),
        ]
        for word, expected in test_cases:
            syllables = split_into_syllables(word.upper())
            assert all(dg in ''.join(syllables) for dg in ["CH", "SH", "DH"] if dg in word.upper())
    
    def test_syllable_empty_input(self):
        assert split_into_syllables("") == []
        assert split_into_syllables("   ") == []


class TestWordValidation:
    
    def test_is_valid_afaan_oromoo_word(self):
        valid_words = [
            "afaan", "oromoo", "dubbachuu", "barreessuu",
            "namoota", "mana", "biyya", "guddaa"
        ]
        invalid_words = [
            "123", "abc123", "word@", "#tag",
            "xyzxyz",
            "bcdfg",
        ]
        for word in valid_words:
            assert is_valid_afaan_oromoo_word(word) is True
        for word in invalid_words:
            assert is_valid_afaan_oromoo_word(word) is False
    
    def test_word_with_diacritics(self):
        assert is_valid_afaan_oromoo_word("Afaan") is True
        assert is_valid_afaan_oromoo_word("Oromoo") is True
    
    def test_word_with_apostrophe(self):
        assert is_valid_afaan_oromoo_word("dha'ii") is True
        assert is_valid_afaan_oromoo_word("ka'aan") is True
    
    @pytest.mark.parametrize("word,expected", [
        ("a", True),
        ("b", True),
        ("ab", True),
        ("ba", True),
        ("aba", True),
    ])
    def test_short_words(self, word, expected):
        assert is_valid_afaan_oromoo_word(word) == expected


class TestAlphabetConstants:
    
    def test_consonants_set(self):
        consonants = QubeeAlphabet.CONSONANTS
        assert isinstance(consonants, set)
        assert len(consonants) == 21
        assert 'B' in consonants
        assert 'C' in consonants
        assert 'Z' in consonants
        assert 'A' not in consonants
    
    def test_vowels_set(self):
        vowels = QubeeAlphabet.VOWELS
        assert isinstance(vowels, set)
        assert len(vowels) == 5
        assert all(vowel in vowels for vowel in ['A', 'E', 'I', 'O', 'U'])
        assert 'B' not in vowels
    
    def test_digraphs_set(self):
        digraphs = QubeeAlphabet.DIGRAPHS
        assert isinstance(digraphs, set)
        assert 'CH' in digraphs
        assert 'SH' in digraphs
        assert 'DH' in digraphs
        assert 'NY' in digraphs
    
    def test_diacritics_dict(self):
        diacritics = QubeeAlphabet.DIACRITICS
        assert isinstance(diacritics, dict)
        assert 'Á' in diacritics
        assert 'á' in diacritics
        assert diacritics['Á'] == 'A'
        assert diacritics['é'] == 'e'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
