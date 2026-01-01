import pytest
import shutil
from pathlib import Path

from qubee_nlp.corpus import (
    AfaanOromooCorpusBuilder,
    CorpusBuilder,
    CorpusLoader,
    CorpusProcessor,
    CorpusSaver,
)

RAW_DIR = Path("test_corpus_raw")
PROCESSED_DIR = Path("test_corpus_processed")


@pytest.fixture(scope="module")
def cleanup_dirs():
    """Ensure clean test directories before and after tests"""
    for d in [RAW_DIR, PROCESSED_DIR]:
        if d.exists():
            shutil.rmtree(d)
    yield
    for d in [RAW_DIR, PROCESSED_DIR]:
        if d.exists():
            shutil.rmtree(d)


def test_full_pipeline(cleanup_dirs):
    # 1️⃣ Build raw corpus
    builder = AfaanOromooCorpusBuilder(output_dir=RAW_DIR)
    raw_data = builder.run_complete_pipeline()
    assert isinstance(raw_data, dict)
    assert all(isinstance(v, list) for v in raw_data.values())
    assert all("content" in item for lst in raw_data.values() for item in lst)

    # 2️⃣ Save raw corpus
    raw_writer = CorpusBuilder(output_dir=RAW_DIR)
    raw_writer.save(raw_data)
    assert any(RAW_DIR.glob("*.txt"))

    # 3️⃣ Load raw corpus
    loader = CorpusLoader(corpus_dir=RAW_DIR)
    loaded = loader.load()
    assert loaded
    for docs in loaded.values():
        assert all(isinstance(d, str) for d in docs)

    # 4️⃣ Process corpus
    processor = CorpusProcessor()
    processed = processor.process(loaded)
    assert processed
    for cat_docs in processed.values():
        for doc in cat_docs:
            assert "original" in doc
            assert "normalized" in doc
            assert "tokens" in doc
            assert "stems" in doc

    # 5️⃣ Save processed corpus
    saver = CorpusSaver(output_dir=PROCESSED_DIR)
    path = saver.save(processed)
    path = Path(path)  # ensure Path object
    assert path.exists()
    # assert JSON files exist
    json_files = list(path.glob("*.json"))
    assert json_files, "No JSON files saved in processed directory"


if __name__ == "__main__":
    pytest.main(["-v", __file__])
