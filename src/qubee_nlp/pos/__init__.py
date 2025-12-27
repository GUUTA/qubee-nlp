"""
Part-of-Speech tagging module for Afaan Oromoo.
"""

# Import taggers
from .tagger import QubeePOSTagger, UnigramTagger, BigramTagger, TrigramTagger

# Import tagsets and utilities
from .tagsets import (
    POS_TAGSET,
    UNIVERSAL_TAGSET,
    get_tag_description,
    validate_tag,
    map_to_universal,
    get_all_tags
)

# Alias for backward compatibility
POSTagger = QubeePOSTagger

# Provide get_afaan_oromoo_tags for tests / legacy code
def get_afaan_oromoo_tags() -> dict:
    """
    Return a dictionary of all Afaan Oromoo POS tags with descriptions.
    Format: {tag: description}
    """
    return {tag: info['description'] for tag, info in POS_TAGSET.items()}

# Public API
__all__ = [
    'QubeePOSTagger',
    'POSTagger',
    'UnigramTagger',
    'BigramTagger',
    'TrigramTagger',
    'POS_TAGSET',
    'UNIVERSAL_TAGSET',
    'get_tag_description',
    'validate_tag',
    'map_to_universal',
    'get_afaan_oromoo_tags'
]
