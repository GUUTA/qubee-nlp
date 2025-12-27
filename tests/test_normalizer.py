"""
Tests for Qubee normalizer module (apostrophes preserved, correct whitespace & diacritics).
"""
import pytest
from qubee_nlp.normalizer import TextNormalizer, normalize_text, remove_diacritics


class TestTextNormalizer:
    """Test TextNormalizer class."""

    def test_normalizer_initialization(self):
        normalizer = TextNormalizer()
        assert normalizer is not None
        assert hasattr(normalizer, 'normalize')

    def test_normalize_basic(self):
        normalizer = TextNormalizer()
        test_cases = [
            ("  Afaan   Oromoo  ", "AFAAN OROMOO"),
            ("\tOromiyaa\n", "OROMIYAA"),
            ("Biyya  guddaa  Afriikaa", "BIYYA GUDDAA AFRIIKAA"),
            ("Akkam jirta?", "AKKAM JIRTA?"),
        ]
        for input_text, expected in test_cases:
            assert normalizer.normalize(input_text) == expected

    def test_normalize_with_diacritics(self):
        normalizer = TextNormalizer()
        assert normalizer.normalize("Áfáan Órómóó") == "AFAAN OROMOO"
        assert normalizer.normalize("Cáffée íbidda") == "CAFFEE IBIDDA"
        assert normalizer.normalize("Tóórbán") == "TOORBAN"

    def test_normalize_preserve_case(self):
        normalizer = TextNormalizer(preserve_case=True)
        assert normalizer.normalize("Áfáan Oromoo") == "Afaan Oromoo"
        assert normalizer.normalize("AkKaM JiRtA") == "AkKaM JiRtA"

    def test_normalize_remove_punctuation(self):
        normalizer = TextNormalizer(remove_punctuation=True)
        assert normalizer.normalize("Akkam jirta?") == "AKKAM JIRTA"
        assert normalizer.normalize("Galatoomaa!") == "GALATOOMAA"

    def test_normalize_keep_punctuation(self):
        normalizer = TextNormalizer(remove_punctuation=False)
        assert normalizer.normalize("Akkam jirta?") == "AKKAM JIRTA?"
        assert normalizer.normalize("Namoonni... dubbatu.") == "NAMOONNI... DUBBATU."

    def test_normalize_special_characters(self):
        normalizer = TextNormalizer()
        # apostrophes preserved
        assert normalizer.normalize("dha'ii") == "DHA'II"
        assert normalizer.normalize("Re'ee ta'e") == "RE'EE TA'E"
        assert normalizer.normalize("afaan-afaan") == "AFAAN-AFAAN"

    def test_normalize_remove_special_chars(self):
        normalizer = TextNormalizer(remove_special_chars=True)
        # apostrophes still preserved
        assert normalizer.normalize("dha'ii") == "DHA'II"
        assert normalizer.normalize("Re'ee ta'e") == "RE'EE TA'E"
        # hyphens replaced by space
        assert normalizer.normalize("afaan-afaan") == "AFAAN AFAAN"

    def test_normalize_empty_input(self):
        normalizer = TextNormalizer()
        assert normalizer.normalize("") == ""
        assert normalizer.normalize("   ") == ""

    def test_normalize_numbers(self):
        normalizer = TextNormalizer()
        assert normalizer.normalize("sadi 3") == "SADI 3"
        assert normalizer.normalize("waggaa 2024") == "WAGGAA 2024"

    def test_normalize_remove_numbers(self):
        normalizer = TextNormalizer(remove_numbers=True)
        assert normalizer.normalize("sadi 3") == "SADI"
        assert normalizer.normalize("123 456") == ""

    def test_normalize_combined_options(self):
        normalizer = TextNormalizer(
            preserve_case=True,
            remove_punctuation=True,
            remove_special_chars=True,
            remove_numbers=True
        )
        text = "Áfáan Oromoo, waggaa 2024! dha'ii Re'ee ta'e 123."
        normalized = normalizer.normalize(text)
        assert normalized == "Afaan Oromoo waggaa dha'ii Re'ee ta'e"

    def test_normalize_whitespace_handling(self):
        normalizer = TextNormalizer()
        test_cases = [
            ("a  b   c", "A B C"),
            ("a\tb\nc", "A B C"),
            ("a\u200bb", "A B"),  # zero-width space replaced with normal space
        ]
        for input_text, expected in test_cases:
            assert normalizer.normalize(input_text) == expected

    def test_normalize_unicode(self):
        normalizer = TextNormalizer()
        # proper Afaan Oromoo spelling
        assert normalizer.normalize("caafeé") == "CAAFEE"

    def test_normalize_mixed_language(self):
        normalizer = TextNormalizer()
        text = "Afaan Oromoo and English words 123."
        normalized = normalizer.normalize(text)
        assert "AFAAN OROMOO" in normalized
        assert "AND ENGLISH WORDS" in normalized
        assert "123" in normalized


class TestRemoveDiacritics:
    """Test remove_diacritics function."""

    def test_remove_diacritics_basic(self):
        assert remove_diacritics("Áfáan") == "Afaan"
        assert remove_diacritics("Órómóó") == "Oromoo"

    def test_remove_diacritics_mixed(self):
        assert remove_diacritics("Áfáan Órómóó dha") == "Afaan Oromoo dha"

    def test_remove_diacritics_no_diacritics(self):
        assert remove_diacritics("Afaan Oromoo") == "Afaan Oromoo"

    def test_remove_diacritics_empty(self):
        assert remove_diacritics("") == ""


class TestNormalizeTextFunction:
    """Test normalize_text convenience function."""

    def test_normalize_text_basic(self):
        assert normalize_text("  Afaan Oromoo  ") == "AFAAN OROMOO"

    def test_normalize_text_with_options(self):
        result = normalize_text("Áfáan Oromoo", preserve_case=True)
        assert result == "Afaan Oromoo"
        result = normalize_text("Akkam jirta?", remove_punctuation=True)
        assert result == "AKKAM JIRTA"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
