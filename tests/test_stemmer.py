import pytest
from qubee_nlp.stemmer import QubeeStemmer, stem_word, lemmatize_word, get_word_root

@pytest.fixture
def stemmer():
    return QubeeStemmer()

def test_stem_basic(stemmer):
    assert stemmer.stem("dhufan") == "DHUF"
    assert stemmer.stem("dhaqan") == "DHAQ"
    assert stemmer.stem("beekan") == "BEEK"
    assert stemmer.stem("jedhan") == "JEDH"
    assert stemmer.stem("argatan") == "ARGAT"
    assert stemmer.stem("bar") == "BAR"
    assert stemmer.stem("him") == "HIM"

def test_stem_aggressive():
    word = "baratan"
    stemmed = stem_word(word, aggressive=True)
    assert stemmed in ["BARAT", "BAR"]

def test_lemmatize_basic(stemmer):
    assert stemmer.lemmatize("dhaqan", pos="VERB").endswith("UU")
    assert stemmer.lemmatize("argatan", pos="VERB").endswith("UU")
    assert stemmer.lemmatize("manawwan", pos="NOUN") == "MANA"
    assert stemmer.lemmatize("manaoota", pos="NOUN") == "MANA"
    assert stemmer.lemmatize("manaota", pos="NOUN") == "MANA"
    assert stemmer.lemmatize("manneeni", pos="NOUN") == "MANA"
    assert stemmer.lemmatize("beektoota", pos="NOUN") == "BEEK"
    assert stemmer.lemmatize("re'oota", pos="NOUN") == "RE'E"

def test_get_root(stemmer):
    assert get_word_root("dhufan") == "DHUF"
    assert get_word_root("beekan") == "BEEK"
    assert get_word_root("manaota") == "MANA"
    assert get_word_root("manneeni") == "MANA"
    assert get_word_root("aa") == "AA"

def test_is_verb_noun(stemmer):
    assert stemmer.is_verb("dhufan") is True
    assert stemmer.is_verb("manaota") is False
    assert stemmer.is_noun("manaota") is True
    assert stemmer.is_noun("dhufan") is False

def test_convenience_functions():
    assert stem_word("dhufan") == "DHUF"
    lemma = lemmatize_word("dhaqan", pos="VERB")
    assert lemma.endswith("UU")
    root = get_word_root("argatan")
    assert root == "ARGAT"

def test_irregular_forms(stemmer):
    assert stemmer.stem("dhufan") == "DHUF"
    assert stemmer.stem("fidan") == "FID"
    assert stemmer.stem("kennan") == "KENN"

def test_short_words(stemmer):
    assert stemmer.stem("aa") == "AA"
    assert stemmer.stem("i") == "I"

def test_non_standard_suffixes(stemmer):
    assert stemmer.stem("dhufetti") == "DHUF"
    assert stemmer.stem("beekanii") == "BEEK"
    assert stemmer.stem("argatanii") == "ARGAT"
