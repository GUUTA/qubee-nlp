# Afaan Oromoo Corpus
## Overview

Qubee-NLP is developed and evaluated using a large-scale Afaan Oromoo corpus containing over 50,000 sentences.

The Qubee-NLP Corpus module provides a complete pipeline for building, processing, and saving Afaan Oromoo NLP corpora. It supports:

* Building raw text corpora
* Loading and saving corpora
* Text normalization
* Tokenization
* Stemming
## Data Collection

The corpus was collected from diverse publicly available sources, including:

* News media
* Educational texts
* Government publications
* Encyclopedic content

## Linguistic Coverage

The dataset represents:

* Multiple registers of Afaan Oromoo

* Orthographic variations in Qubee

* Rich morphological structures

## Role in Qubee-NLP

* The corpus is used for:
* Unit testing preprocessing modules
* Rule validation for stemming and syllabification
* Baseline machine learning experiments

## How to Use the Corpus with Qubee-NLP

The following workflow demonstrates how to integrate the corpus with the tokenizer, stemmer, and normalizer.
```python
#Import Modules
from qubee_nlp.corpus.afaan_oromoo_nlp_corpus import quick_build
from qubee_nlp.tokenizer import QubeeTokenizer
from qubee_nlp.stemmer import QubeeStemmer
from qubee_nlp.normalizer import TextNormalizer
```
## Build the Corpus
corpus = quick_build(output_dir="my_afaan_oromoo_corpus")

```
corpus is now a dictionary of categories:
```python
print(corpus.keys())
# dict_keys(['university', 'news_media', 'government', 'cultural', 'alternative', 'processed'])
```
### Initialize NLP Components
```python
tokenizer = QubeeTokenizer()     # Tokenizer for Afaan Oromoo text
stemmer = QubeeStemmer()         # Rule-based stemmer
normalizer = TextNormalizer()    # Normalizes spelling, punctuation, and special characters
```
## Process Corpus Step by Step
```python
processed_corpus = {}

for category, articles in corpus.items():
    processed_corpus[category] = []
    for article in articles:
        text = article.get("content", "")
        title = article.get("title", "")
        source = article.get("source", "")
        
        # 1️⃣ Normalize text
        norm_text = normalizer.normalize(text)
        
        # 2️⃣ Tokenize text
        tokens = tokenizer.tokenize(norm_text)
        
        # 3️⃣ Stem each token
        stems = [stemmer.stem(tok) for tok in tokens]
        
        # Save processed article
        processed_corpus[category].append({
            "title": title,
            "original": text,
            "normalized": norm_text,
            "tokens": tokens,
            "stems": stems,
            "source": source,
        })

```
✅ processed_corpus now contains everything: original, normalized, tokenized, and stemmed words.
```python
#Inspect a Processed Article
first_article = processed_corpus['university'][0]
print("Title:", first_article['title'])
print("Original:", first_article['original'])
print("Normalized:", first_article['normalized'])
print("Tokens:", first_article['tokens'])
print("Stems:", first_article['stems'])
```

Example Output (stub data):
```python
Title: university example
Original: Kun Afaan Oromoo fakkeenya barruu dha.
Normalized: KUN AFAAN OROMOO FAKKEENYA BARRUU DHA
Tokens: ['KUN', 'AFAAN', 'OROMOO', 'FAKKEENYA', 'BARRUU', 'DHA']
Stems: ['KUN', 'AFAAN', 'OROM', 'FAKKEENYA', 'BARR', 'DHA']
```
## Full End-to-End Usage Script
```python
from qubee_nlp.corpus.afaan_oromoo_nlp_corpus import AfaanOromooCorpusBuilder
from qubee_nlp.corpus.corpus_builder import CorpusBuilder
from qubee_nlp.corpus.loaders import CorpusLoader
from qubee_nlp.corpus.corpus_processor import CorpusProcessor
from qubee_nlp.corpus.corpus_saver import CorpusSaver
from pathlib import Path

# 1️⃣ Build raw corpus
builder = AfaanOromooCorpusBuilder(output_dir=Path("raw_corpus"))
raw_data = builder.run_complete_pipeline()

# 2️⃣ Save raw corpus
raw_writer = CorpusBuilder(output_dir=Path("raw_corpus"))
raw_writer.save(raw_data)

# 3️⃣ Load raw corpus
loader = CorpusLoader(corpus_dir=Path("raw_corpus"))
raw_text = loader.load()

# 4️⃣ Process corpus
processor = CorpusProcessor()
processed = processor.process(raw_text)

# 5️⃣ Save processed corpus
output_dir = Path("processed_corpus")
saver = CorpusSaver(output_dir=output_dir)
output_path = saver.save(processed)

print("✔ Corpus pipeline completed. Saved to:", output_path)