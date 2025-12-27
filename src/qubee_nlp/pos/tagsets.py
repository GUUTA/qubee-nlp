"""
POS tag sets for Afaan Oromoo (Oromo language).
"""

from typing import Dict
from types import MappingProxyType

# Universal POS tags
UNIVERSAL_TAGSET: Dict[str, str] = {
    'NOUN': 'Noun',
    'VERB': 'Verb',
    'ADJ': 'Adjective',
    'ADV': 'Adverb',
    'PRON': 'Pronoun',
    'DET': 'Determiner',
    'ADP': 'Adposition',
    'CONJ': 'Conjunction',
    'PRT': 'Particle',
    'INTJ': 'Interjection',
    'NUM': 'Numeral',
    'PUNC': 'Punctuation',
    'X': 'Other'
}

# Afaan Oromoo POS tags mapped to universal tags
POS_TAGSET: Dict[str, Dict[str, str]] = {
    # Nouns
    'NN': {'description': 'Common noun', 'universal': 'NOUN'},
    'NNC': {'description': 'Count noun', 'universal': 'NOUN'},
    'NNM': {'description': 'Mass noun', 'universal': 'NOUN'},
    'NPROP': {'description': 'Proper noun', 'universal': 'NOUN'},
    'NPL': {'description': 'Plural noun', 'universal': 'NOUN'},

    # Pronouns
    'PPER': {'description': 'Personal pronoun', 'universal': 'PRON'},
    'PDEM': {'description': 'Demonstrative pronoun', 'universal': 'PRON'},
    'PINT': {'description': 'Interrogative pronoun', 'universal': 'PRON'},
    'PREL': {'description': 'Relative pronoun', 'universal': 'PRON'},
    'POSS': {'description': 'Possessive pronoun', 'universal': 'PRON'},
    'PREFL': {'description': 'Reflexive pronoun', 'universal': 'PRON'},

    # Verbs
    'VB': {'description': 'Base form verb', 'universal': 'VERB'},
    'VBF': {'description': 'Finite verb', 'universal': 'VERB'},
    'VBINF': {'description': 'Infinitive verb', 'universal': 'VERB'},
    'VBIMP': {'description': 'Imperative verb', 'universal': 'VERB'},
    'VBPART': {'description': 'Participial verb', 'universal': 'VERB'},
    'VBCAUS': {'description': 'Causative verb', 'universal': 'VERB'},
    'VBPASS': {'description': 'Passive verb', 'universal': 'VERB'},
    'VBREFL': {'description': 'Reflexive verb', 'universal': 'VERB'},
    'VBAUX': {'description': 'Auxiliary verb', 'universal': 'VERB'},

    # Adjectives
    'JJ': {'description': 'Adjective', 'universal': 'ADJ'},
    'JJC': {'description': 'Comparative adjective', 'universal': 'ADJ'},
    'JJS': {'description': 'Superlative adjective', 'universal': 'ADJ'},
    'JJNUM': {'description': 'Numeral adjective', 'universal': 'ADJ'},
    'JJPOSS': {'description': 'Possessive adjective', 'universal': 'ADJ'},

    # Adverbs
    'RB': {'description': 'Adverb', 'universal': 'ADV'},
    'RBC': {'description': 'Comparative adverb', 'universal': 'ADV'},
    'RBS': {'description': 'Superlative adverb', 'universal': 'ADV'},
    'RBINT': {'description': 'Interrogative adverb', 'universal': 'ADV'},
    'RBNEG': {'description': 'Negative adverb', 'universal': 'ADV'},

    # Determiners
    'DT': {'description': 'Determiner', 'universal': 'DET'},
    'DTDEM': {'description': 'Demonstrative determiner', 'universal': 'DET'},
    'DTINT': {'description': 'Interrogative determiner', 'universal': 'DET'},
    'DTPOSS': {'description': 'Possessive determiner', 'universal': 'DET'},
    'DTIND': {'description': 'Indefinite determiner', 'universal': 'DET'},

    # Adpositions
    'IN': {'description': 'Preposition', 'universal': 'ADP'},
    'POST': {'description': 'Postposition', 'universal': 'ADP'},

    # Conjunctions
    'CC': {'description': 'Coordinating conjunction', 'universal': 'CONJ'},
    'CS': {'description': 'Subordinating conjunction', 'universal': 'CONJ'},

    # Particles
    'RP': {'description': 'Particle', 'universal': 'PRT'},
    'NEG': {'description': 'Negative particle', 'universal': 'PRT'},
    'FOC': {'description': 'Focus particle', 'universal': 'PRT'},
    'Q': {'description': 'Question particle', 'universal': 'PRT'},

    # Interjections
    'UH': {'description': 'Interjection', 'universal': 'INTJ'},

    # Numerals
    'CD': {'description': 'Cardinal number', 'universal': 'NUM'},
    'OD': {'description': 'Ordinal number', 'universal': 'NUM'},

    # Other
    'FW': {'description': 'Foreign word', 'universal': 'X'},
    'SYM': {'description': 'Symbol', 'universal': 'X'},
    'LS': {'description': 'List item marker', 'universal': 'X'},

    # Punctuation
    '.': {'description': 'Sentence-final punctuation', 'universal': 'PUNC'},
    ',': {'description': 'Comma', 'universal': 'PUNC'},
    ':': {'description': 'Colon', 'universal': 'PUNC'},
    ';': {'description': 'Semicolon', 'universal': 'PUNC'},
    '``': {'description': 'Opening quote', 'universal': 'PUNC'},
    "''": {'description': 'Closing quote', 'universal': 'PUNC'},
    '(': {'description': 'Opening parenthesis', 'universal': 'PUNC'},
    ')': {'description': 'Closing parenthesis', 'universal': 'PUNC'},
}

# Common verb suffixes
VERB_SUFFIXES = {
    'uu': 'VBINF',
    'aa': 'VBF',
    'ee': 'VBF',
    'i': 'VBIMP',
    'u': 'VBPART',
    'si': 'VBCAUS',
    'am': 'VBPASS',
    'at': 'VBREFL',
}

# Common noun suffixes
NOUN_SUFFIXES = {
    'ii': 'NPL',
    'ww': 'NPL',
    'aa': 'NN',
    'oo': 'NN',
    'uu': 'NN',
}

# Return description of an Afaan Oromoo tag
def get_tag_description(tag: str):
    info = POS_TAGSET.get(tag)
    return info['description'] if info else None

# Return universal tag for an Afaan Oromoo tag
def get_universal_tag(tag: str):
    info = POS_TAGSET.get(tag)
    return info['universal'] if info else None

# Map Afaan Oromoo tag to universal (fallback to 'X')
def map_to_universal(tag: str) -> str:
    utag = get_universal_tag(tag)
    return utag if utag else 'X'

# Validate if tag exists
def validate_tag(tag: str) -> bool:
    return tag in POS_TAGSET

# Get list of all Afaan Oromoo tags
def get_all_tags():
    return list(POS_TAGSET.keys())

# Get tags by universal category
def get_tags_by_category(category: str):
    return [tag for tag, info in POS_TAGSET.items() if info['universal'] == category]

# **Fixed version** for tests: returns list of Afaan Oromoo POS tags
def get_afaan_oromoo_tags():
    """
    Return all Afaan Oromoo POS tags (keys), for testing and validation.
    Previously returned universal tags which caused failed tests.
    """
    return list(POS_TAGSET.keys())
