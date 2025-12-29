# Stemmer API Documentation

## Overview

The **Stemmer module** in `qubee-nlp` provides **rule-based stemming** functionality for **Afaan Oromoo (Qubee)** text.

**Stemming** is the process of reducing inflected or derived words to their **root or base form (stem)** by systematically removing known affixes while preserving the semantic core of the word.

This module is designed to support:

- Text normalization pipelines
- Token preprocessing
- Information retrieval systems
- Text classification
- Search engines
- Language modeling workflows

The stemmer is **lightweight, deterministic, and linguistically motivated**, making it suitable for both **research** and **production** environments.

---

## Motivation

Afaan Oromoo is a **morphologically rich language**. Words frequently encode multiple grammatical meanings through suffixes, including:

- **Plurality**
- **Possession**
- **Case markers**
- **Derivational morphemes**
- **Agentive and nominalizing suffixes**

### Examples

| Word | Meaning | Stem |
|------|--------|------|
| barattoota | students | barat |
| hojjetoota | workers | hojjet |
| mana isaanii | their house | man |
| dubbachuun | speaking | dubb |
| beekamtii | recognition | beek |

Without stemming, NLP systems suffer from:

- Vocabulary explosion
- High sparsity
- Poor generalization
- Reduced recall in search and IR systems

The `qubee-nlp` stemmer addresses these issues by **normalizing surface word forms into stable stems**.

---

## Design Philosophy

The stemmer follows these principles:

1. **Rule-based (not statistical)**  
   Ensures transparency, reproducibility, and linguistic control.

2. **Non-destructive**  
   Removes suffixes conservatively to avoid overstemming.

3. **Deterministic**  
   Same input always yields the same output.

4. **Qubee-aware**  
   Respects Afaan Oromoo phonology and orthography.

5. **Normalizer-compatible**  
   Assumes input is already normalized using `TextNormalizer`.

---

## Module Structure
Main Components

QubeeStemmer — core stemming class

Utility wrapper functions for convenience

Public API
QubeeStemmer
class QubeeStemmer:
    def __init__(self, aggressive: bool = False)

Parameters
Parameter	Type	Description
aggressive	bool	If True, applies deeper suffix stripping (riskier)
stem_word
stem_word(word: str, aggressive: bool = False) -> str


Returns the stem of a single word.

Example
from qubee_nlp import stem_word

stem_word("barattoota")
# 'barat'

lemmatize_word
lemmatize_word(word: str) -> str


Alias for stem_word. Included for semantic clarity in NLP pipelines.

get_word_root
get_word_root(word: str) -> str


Returns the most reduced root form after suffix removal.

Supported Suffix Categories

The stemmer recognizes and removes suffixes in ordered stages.

1. Plural Markers
-oota
-wwan
-ota


Example

barattoota → barat
namoota → nam

2. Possessive Suffixes
-koo   (my)
-kee   (your)
-isaa  (his)
- ishee (her)
-keenya (our)
- isaanii (their)


Example

mana isaanii → man

3. Case and Functional Endings
-tti
-rra
-f
-fiin


Example

mana irratti → man

4. Derivational and Nominalizers
-ummaa
-amtii
-umsa
-ina


Example

beekamtii → beek

5. Verb-related Endings (Conservative)
-chuu
-chaan
-chuuf


Example

dubbachuun → dubb

Aggressive Mode

When aggressive=True, the stemmer:

Applies additional suffix stripping

Removes shorter and overlapping suffixes

May slightly increase overstemming risk

stem_word("hojjetoota", aggressive=True)
# 'hojjet'