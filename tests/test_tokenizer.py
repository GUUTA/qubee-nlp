# tests/test_tokenizer.py
import pytest
from src.qubee_nlp.tokenizer import QubeeTokenizer, word_tokenize, sentence_tokenize

class TestQubeeTokenizer:

    def test_tokenizer_initialization(self):
        tokenizer = QubeeTokenizer()
        assert tokenizer.preserve_case is False
        assert tokenizer.strict is False

    def test_tokenize_basic(self):
        tokenizer = QubeeTokenizer()
        text = "Afaan Oromoo afaan jalqaba Oromiyaati."
        expected = ['AFAAN', 'OROMOO', 'AFAAN', 'JALQABA', 'OROMIYAATI']
        tokens = tokenizer.tokenize(text)
        assert tokens == expected

    def test_tokenize_with_diacritics(self):
        tokenizer = QubeeTokenizer()
        text = "Café fi résumé"
        tokens = tokenizer.tokenize(text)
        assert tokens == ['CAFE', 'FI', 'RESUME']

    def test_tokenize_preserve_case(self):
        tokenizer = QubeeTokenizer(preserve_case=True)
        text = "Afaan Oromoo"
        tokens = tokenizer.tokenize(text)
        assert tokens == ['Afaan', 'Oromoo']  # Fixed

    def test_tokenize_special_characters(self):
        tokenizer = QubeeTokenizer()
        text = "Hello! #1"
        tokens = tokenizer.tokenize(text)
        assert tokens == ['HELLO']

    def test_tokenize_empty_text(self):
        tokenizer = QubeeTokenizer()
        assert tokenizer.tokenize("") == []

    def test_tokenize_mixed_punctuation(self):
        tokenizer = QubeeTokenizer()
        text = "Hello, world! Afaan."
        tokens = tokenizer.tokenize(text)
        assert tokens == ['HELLO', 'WORLD', 'AFAAN']

    def test_tokenize_strict_mode(self):
        tokenizer = QubeeTokenizer(strict=True)
        text = "Hello 123"
        with pytest.raises(ValueError):
            tokenizer.tokenize(text)

    def test_tokenize_with_positions(self):
        tokenizer = QubeeTokenizer()
        text = "Afaan Oromoo"
        positions = tokenizer.tokenize_with_positions(text)
        assert len(positions) == 2
        assert positions[0]['token'] == 'AFAAN'
        assert positions[1]['token'] == 'OROMOO'

    def test_tokenize_with_context(self):
        tokenizer = QubeeTokenizer()
        text = "Afaan Oromoo"
        tokens = tokenizer.tokenize_with_context(text, context_chars=2)
        assert tokens[0]['left_context'] == ''
        assert tokens[0]['right_context'] == ' O'
        assert tokens[1]['left_context'] == 'n '
        assert tokens[1]['right_context'] == ''

    def test_tokenize_invalid_text(self):
        tokenizer = QubeeTokenizer(strict=True)
        text = "123 @"
        with pytest.raises(ValueError):
            tokenizer.tokenize(text)

    def test_sentence_tokenize_basic(self):
        tokenizer = QubeeTokenizer()
        text = "Afaan Oromoo. Afaan jalqaba Oromiyaati."
        sentences = tokenizer.sentence_tokenize(text)
        expected = ["AFAAN OROMOO.", "AFAAN JALQABA OROMIYAATI."]
        assert sentences == expected

    def test_sentence_tokenize_with_quotes(self):
        tokenizer = QubeeTokenizer()
        text = '"Afaan Oromoo," jedhu.'
        sentences = tokenizer.sentence_tokenize(text)
        assert sentences == ['"AFAAN OROMOO," JEDHU.']

    def test_sentence_tokenize_abbreviations(self):
        tokenizer = QubeeTokenizer()
        text = "Dr. Abebe."
        sentences = tokenizer.sentence_tokenize(text)
        assert sentences == ['DR. ABEBE.']

    def test_sentence_tokenize_empty(self):
        tokenizer = QubeeTokenizer()
        assert tokenizer.sentence_tokenize("") == []

    def test_sentence_tokenize_single_sentence(self):
        tokenizer = QubeeTokenizer()
        text = "Afaan Oromoo afaan jalqaba Oromiyaati."
        sentences = tokenizer.sentence_tokenize(text)
        assert sentences[0] == "AFAAN OROMOO AFAAN JALQABA OROMIYAATI."

    def test_sentence_tokenize_multiline(self):
        tokenizer = QubeeTokenizer()
        text = "Afaan Oromoo.\nAfaan jalqaba Oromiyaati."
        sentences = tokenizer.sentence_tokenize(text)
        expected = ["AFAAN OROMOO.", "AFAAN JALQABA OROMIYAATI."]
        assert sentences == expected


class TestConvenienceFunctions:

    def test_word_tokenize_function(self):
        text = "Afaan Oromoo"
        tokens = word_tokenize(text)
        assert tokens == ['AFAAN', 'OROMOO']

    def test_word_tokenize_with_params(self):
        text = "Afaan Oromoo"
        tokens = word_tokenize(text, preserve_case=True)
        assert tokens == ['Afaan', 'Oromoo']  # Fixed

    def test_sentence_tokenize_function(self):
        text = "Afaan Oromoo. Afaan jalqaba Oromiyaati."
        sentences = sentence_tokenize(text)
        assert sentences == ["AFAAN OROMOO.", "AFAAN JALQABA OROMIYAATI."]

    def test_sentence_tokenize_with_params(self):
        text = "Hello 123"
        with pytest.raises(ValueError):
            sentence_tokenize(text, strict=True)


class TestTokenizerEdgeCases:

    @pytest.mark.parametrize("text,expected_count", [
        ("a", 1),
        ("b", 1),
        ("a b c", 3),
        ("word-with-hyphens", 1),
        ("word'with'apostrophes", 1),
        ("word1word2", 0)
    ])
    def test_token_count(self, text, expected_count):
        tokenizer = QubeeTokenizer(strict=True)
        if expected_count == 0:
            with pytest.raises(ValueError):
                tokenizer.tokenize(text)
        else:
            tokens = tokenizer.tokenize(text)
            assert len(tokens) == expected_count

    def test_tokenize_very_long_text(self):
        tokenizer = QubeeTokenizer()
        text = "Afaan " * 1000
        tokens = tokenizer.tokenize(text)
        assert len(tokens) == 1000

    def test_tokenize_unicode_boundary(self):
        tokenizer = QubeeTokenizer()
        text = "Café résumé"
        tokens = tokenizer.tokenize(text)
        assert tokens == ['CAFE', 'RESUME']

    def test_tokenize_mixed_languages(self):
        tokenizer = QubeeTokenizer()
        text = "Afaan Oromoo English text"
        tokens = tokenizer.tokenize(text)
        assert tokens == ['AFAAN', 'OROMOO', 'ENGLISH', 'TEXT']


# ---------------------------
# Main
# ---------------------------
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
