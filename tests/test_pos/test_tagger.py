"""
Tests for POS tagger.
"""

import pytest
from qubee_nlp.pos.tagger import QubeePOSTagger
from qubee_nlp.pos.tagsets import get_all_tags, get_tag_description


class TestPOSTagger:
    """Test QubeePOSTagger class."""

    def test_initialization(self):
        tagger = QubeePOSTagger()
        assert tagger is not None
        assert hasattr(tagger, 'model')

    def test_tag_basic(self):
        tagger = QubeePOSTagger()
        tokens = ["Oromoon", "Afaan", "Oromootiin", "dubbatu"]
        tags = tagger.tag(tokens)
        assert isinstance(tags, list)
        assert len(tags) == len(tokens)
        valid_tags = ['NOUN', 'VERB', 'ADJ', 'ADV', 'PRON', 'DET',
                      'CONJ', 'PRT', 'PUNC', 'ADP', 'X', 'UNK', 'NUM']
        assert all(tag in valid_tags for tag in tags)

    def test_tag_with_unknown_words(self):
        tagger = QubeePOSTagger()
        tokens = ["Xyz", "123", "!@#", "Oromoo"]
        tags = tagger.tag(tokens)
        assert len(tags) == len(tokens)
        assert tags[0] in ['UNK', 'X', 'NOUN']
        assert tags[1] == 'NUM'
        assert tags[2] in ['UNK', 'PUNC', 'X']
        assert tags[3] in ['NOUN', 'X', 'UNK']

    def test_tag_empty(self):
        tagger = QubeePOSTagger()
        assert tagger.tag([]) == []
        assert tagger.tag([""]) == ["UNK"]

    def test_tag_single_word(self):
        tagger = QubeePOSTagger()
        test_words = ["Oromoo", "dubbatu", "guddaa", "keessa"]
        expected_tags = ['NOUN', 'VERB', 'ADJ', 'ADP']
        for word, expected in zip(test_words, expected_tags):
            tags = tagger.tag([word])
            assert tags[0] == expected  # exact match now

    def test_tag_with_context(self):
        tagger = QubeePOSTagger()
        tokens1 = ["barreessaa", "kitaaba"]
        tokens2 = ["barreessaa", "guddaa"]
        tags1 = tagger.tag(tokens1)
        tags2 = tagger.tag(tokens2)
        valid_tags = ['NOUN', 'VERB', 'ADJ', 'ADV', 'PRON',
                      'DET', 'CONJ', 'PRT', 'PUNC', 'ADP', 'X', 'UNK']
        assert all(tag in valid_tags for tag in tags1 + tags2)


class TestTagSet:
    """Test tag set functionality."""

    def test_get_afaan_oromoo_tags(self):
        tags = get_all_tags()
        for tag in ['NN', 'VB', 'JJ', 'RB', 'DT']:
            assert tag in tags

    def test_tag_descriptions(self):
        for tag in ['NN', 'VB', 'JJ']:
            desc = get_tag_description(tag)
            assert desc is not None
            assert isinstance(desc, str)
            assert len(desc) > 0

    def test_tag_consistency(self):
        tags = get_all_tags()
        try:
            tags.append("NEW_TAG")
        except Exception:
            pytest.fail("Appending to tag list should not raise exception")


class TestPOSTaggerEdgeCases:
    """Test POS tagger edge cases."""

    def test_tag_with_special_characters(self):
        tagger = QubeePOSTagger()
        tokens = ["waa'ee", "afaan-jalqaba", "biyya-keessa", "@", "#"]
        tags = tagger.tag(tokens)
        expected_tags = ['NOUN', 'NOUN', 'NOUN', 'PUNC', 'PUNC']
        assert tags == expected_tags  # exact match for clarity

    def test_tag_with_numbers(self):
        tagger = QubeePOSTagger()
        tokens = ["tokko", "lama", "sadi", "123", "45.6"]
        tags = tagger.tag(tokens)
        expected_tags = ['NUM', 'NUM', 'NUM', 'NUM', 'NUM']
        assert tags == expected_tags

    def test_tag_mixed_case(self):
        tagger = QubeePOSTagger()
        tokens = ["Oromoo", "oromoo", "OROMOO", "oRoMoO"]
        tags = tagger.tag(tokens)
        expected_tags = ['NOUN', 'NOUN', 'NOUN', 'NOUN']
        assert tags == expected_tags
