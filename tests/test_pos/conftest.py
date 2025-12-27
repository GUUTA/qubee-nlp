import pytest
from pathlib import Path

# Test data directory
TEST_DATA_DIR = Path(__file__).parent / "test_data"
TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)

@pytest.fixture
def sample_afaan_oromoo_texts():
    return {
        "simple": "Afaan Oromoo afaan guddaa dha.",
        "with_diacritics": "Áfáan Órómóó gúddáa dha.",
        "with_apostrophe": "Waa'ee dubbiin kana dubbachuun barbaachisaa dha.",
        "with_hyphen": "Afaan-jalqaba Oromiyaa keessatti dha.",
        "multiple_sentences": "Kuni kitaaba dha. Inni bareessaa dha. Galatoomaa!",
        "long_text": """
        Afaan Oromoo afaan Kushitikii kan dubbatamu Oromiyaa fi naannawa ishee keessatti dha.
        Afaanichi afaan baayyinaan dubbatamu Afriikaa keessatti, Afrikaa Kibbaa fi Kaabaati.
        Qubee sirna barreeffama Afaan Oromoo sirna Laatin irratti hundaa'e dha.
        """,
        "invalid_text": "Afaan Oromoo 123 test! @#$",
        "mixed_case": "Afaan Oromoo Afaan Guddaa Dha.",
        "whitespace": "  Afaan   Oromoo   guddaa   dha.  ",
    }

@pytest.fixture
def sample_words():
    return {
        "simple": ["Oromoo", "Afaan", "guddaa", "dha"],
        "complex": ["barreessuu", "dubbachuu", "guddina", "jiraachuu"],
        "with_diacritics": ["Áfáan", "Órómóó", "gúddáa"],
        "with_apostrophe": ["waa'ee", "dha'ima", "maqaa'ee"],
        "with_hyphen": ["afaan-jalqaba", "biyya-keessa", "mana-barumsaa"],
        "digraphs": ["chibbuu", "dhaga'uu", "khayrii", "nyaata", "shamarree", "tsaboo"],
    }

@pytest.fixture(scope="session")
def qubee_alphabet():
    from qubee_nlp.alphabet import QubeeAlphabet
    return QubeeAlphabet

@pytest.fixture(scope="session")
def tokenizer():
    from qubee_nlp.tokenizer import QubeeTokenizer
    return QubeeTokenizer()

@pytest.fixture(scope="session")
def stemmer():
    from qubee_nlp.stemmer import QubeeStemmer
    return QubeeStemmer()

@pytest.fixture
def sample_corpus_file(tmp_path):
    corpus_content = """
    Afaan Oromoo afaan guddaa dha.
    Oromiyaan biyya guddaa Afriikaa keessatti argamti.
    Qubee sirna barreeffama Afaan Oromoo dha.
    Barreessitootni kitaaba bareessan.
    """
    corpus_file = tmp_path / "test_corpus.txt"
    corpus_file.write_text(corpus_content, encoding="utf-8")
    return str(corpus_file)

# Register markers
def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "performance: mark test as performance benchmark")
    config.addinivalue_line("markers", "requires_data: test requires external data")

# Skip slow/integration tests by default
def pytest_collection_modifyitems(config, items):
    if not config.getoption("--run-slow"):
        skip_slow = pytest.mark.skip(reason="need --run-slow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)
    if not config.getoption("--run-integration"):
        skip_integration = pytest.mark.skip(reason="need --run-integration option to run")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)

# Command line options
def pytest_addoption(parser):
    parser.addoption("--run-slow", action="store_true", default=False, help="run slow tests")
    parser.addoption("--run-integration", action="store_true", default=False, help="run integration tests")
